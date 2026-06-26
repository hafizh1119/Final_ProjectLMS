from typing import Optional
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from ninja import NinjaAPI
from ninja.errors import HttpError
from django.core.cache import cache
import hashlib
import json
from django.utils import timezone

from courses.models import Course, CourseMember, CourseContent, CourseContentCompletion, Category, CourseReview,CourseWishlist,CourseModule
from courses.schemas import *
from courses.auth import auth, create_token, decode_token
from courses.permissions import *
from courses.helpers import get_object_or_404

# Import untuk advanced features
from lms.throttle import RedisRateThrottle
from services.logging_service import log_activity, get_user_activities
from services.analytics_service import record_content_view, get_popular_courses
from .tasks import send_enrollment_email, generate_certificate, export_course_report, update_course_statistics

api = NinjaAPI(
    title="Simple LMS API",
    version="1.0.0",
)


# ================= USER HELPER =================

def user_dict(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": get_role(user),
    }


# ================= AUTH =================

@api.post("/auth/register")
def register(request, data: RegisterIn):
    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, "Username used")

    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name,
    )

    # PERBAIKAN: Jika role "teacher", gunakan group "instructor"
    if data.role == "teacher":
        group_name = "instructor"
    else:
        group_name = data.role
    
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)

    return user_dict(user)


@api.post("/auth/login")
def login(request, data: LoginIn):
    user = authenticate(username=data.username, password=data.password)

    if not user:
        raise HttpError(401, "Login gagal")

    return {
        "access": create_token(user),
        "refresh": create_token(user, "refresh"),
    }


@api.post("/auth/refresh")
def refresh_token(request, data: RefreshIn):
    payload = decode_token(data.refresh)
    user = get_object_or_404(User, id=payload["user_id"])

    return {
        "access": create_token(user),
        "refresh": create_token(user, "refresh"),
    }


@api.get("/auth/me", auth=auth)
def me(request):
    return user_dict(request.auth)


@api.put("/auth/me", auth=auth)
def update_me(request, data: ProfileUpdateIn):
    user = request.auth

    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name
    if data.email is not None:
        user.email = data.email

    user.save()
    return user_dict(user)

# ================= INSTRUCTORS =================

@api.get(
    "/instructors",
    response=List[InstructorOut],
    summary="Daftar Dosen"
)
def list_instructors(request):

    instructors = User.objects.filter(
        groups__name="instructor"
    )

    return [
        {
            "id": user.id,
            "username": user.username,
            "full_name": f"{user.first_name} {user.last_name}".strip()
        }
        for user in instructors
    ]
# ================= COURSES =================

@api.get("/courses", summary="Pencarian dan Filter Course",)
def list_courses(
    request,
    search: Optional[str] = None,
    category: Optional[int] = None,
    teacher: Optional[int] = None,
    sort: Optional[str] = None,
    level: Optional[str] = None,
    status: Optional[str] = None,
):
    qs = Course.objects.all()

    if search:
        qs = qs.filter(name__icontains=search)

    if category:
        qs = qs.filter(category_id=category)

    if teacher:
        qs = qs.filter(teacher_id=teacher)

    if sort:
        allowed = [
            "price",
            "-price",
            "created_at",
            "-created_at",
        ]

        if sort in allowed:
            qs = qs.order_by(sort)
    
    if level:
        qs = qs.filter(level=level)

    if status:
        qs = qs.filter(status=status)

    return {
        "count": qs.count(),
        "results": [CourseOut.from_orm(c) for c in qs],
    }

@api.get("/courses/{id}")
def detail_course(request, id: int):
    cache_key = f"course:{id}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    course = get_object_or_404(Course, id=id)
    result = CourseOut.from_orm(course)
    cache.set(cache_key, result, 300)
    return result

@api.post("/courses", auth=auth)
def create_course(request, data: CourseIn):
    is_instructor(request.auth)

    course = Course.objects.create(
        name=data.name,
        description=data.description,
        price=data.price,
        category_id=data.category_id,
        level=data.level,
        status=data.status,
        teacher=request.auth,
    )
    cache.delete_pattern("courses:list:*")

    return CourseOut.from_orm(course)


@api.patch("/courses/{id}", auth=auth)
def update_course(request, id: int, data: CoursePatchIn):
    course = get_object_or_404(Course, id=id)
    is_course_owner(request.auth, course)

    if data.name:
        course.name = data.name
    if data.description:
        course.description = data.description
    if data.price:
        course.price = data.price
    
    if data.category_id is not None:
        course.category_id = data.category_id

    if data.level is not None:
        course.level = data.level

    if data.status is not None:
        course.status = data.status

    course.save()

    cache.delete_pattern("courses:list:*")
    cache.delete(f"course:{course.id}")

    return CourseOut.from_orm(course)


@api.delete("/courses/{id}", auth=auth)
def delete_course(request, id: int):

    is_admin(request.auth)

    course = get_object_or_404(Course, id=id)

    cache.delete_pattern("courses:list:*")
    cache.delete(f"course:{id}")

    course.delete()

    return {"success": True}

# ================= CATEGORIES =================

@api.get("/categories", response=List[CategoryOut])
def list_categories(request):
    return Category.objects.all()


@api.post("/categories", auth=auth, response=CategoryOut)
def create_category(request, data: CategoryIn):
    is_admin(request.auth)

    category = Category.objects.create(
        name=data.name,
        description=data.description,
    )

    return category

# ================= MODULES =================

@api.get("/modules", response=List[ModuleOut], summary="Daftar Module Course")
def list_modules(request):
    return CourseModule.objects.prefetch_related("contents").select_related("course")

@api.post( "/modules", auth=auth, response=ModuleOut)
def create_module(request, data: ModuleIn):

    is_instructor(request.auth)

    module = CourseModule.objects.create(
        course_id=data.course_id,
        title=data.title,
        description=data.description,
        order=data.order,
    )

    return module

# ================= CONTENT =================

@api.get("/lessons", response=List[ContentOut],summary="Daftar Lesson")
def list_contents(request):
    return CourseContent.objects.select_related("course_id", "module")


@api.post("/lessons", auth=auth, response=ContentOut, summary="Create Lesson")
def create_content(request, data: ContentIn):

    is_instructor(request.auth)
    module = get_object_or_404(CourseModule, id=data.module_id)
    content = CourseContent.objects.create(
        course_id=module.course,
        module=module,
        name=data.name,
        description=data.description,
        video_url=data.video_url,
    )

    return content

# ================= ENROLLMENTS =================

@api.post("/enrollments", auth=auth)
def enroll(request, data: EnrollmentIn):
    is_student(request.auth)

    course = get_object_or_404(Course, id=data.course_id)

    if CourseMember.objects.filter(course_id=course, user_id=request.auth).exists():
        raise HttpError(400, "Sudah enroll")

    member = CourseMember.objects.create(
        course_id=course,
        user_id=request.auth,
        roles="std",
    )

    return CourseMemberOut.from_orm(member)


@api.get("/enrollments/my-courses", auth=auth)
def my_courses(request):
    members = CourseMember.objects.filter(user_id=request.auth)
    return [CourseMemberOut.from_orm(m) for m in members]


@api.post("/enrollments/{id}/progress", auth=auth)
def progress(request, id: int, data: ProgressIn):
    member = get_object_or_404(CourseMember, id=id)
    content = get_object_or_404(CourseContent, id=data.content_id)

    completion = CourseContentCompletion.objects.create(
        member_id=member,
        content_id=content,
    )
    return CourseContentCompletionOut.from_orm(completion)

# ================= REVIEWS =================

@api.post("/courses/{id}/reviews", auth=auth, response=ReviewOut, summary="Memberikan Review Course")
def create_review(request, id: int, data: ReviewIn):

    course = get_object_or_404(Course, id=id)

    review, created = CourseReview.objects.update_or_create(
        course=course,
        user=request.auth,
        defaults={
            "rating": data.rating,
            "review": data.review,
        }
    )

    return review


@api.get( "/courses/{id}/reviews", response=List[ReviewOut])
def list_reviews(request, id: int):

    course = get_object_or_404(
        Course,
        id=id
    )

    return CourseReview.objects.filter(
        course=course
    )

# ================= ADVANCED FEATURES (REDIS, MONGODB, CELERY) =================

# 1. Cached Courses (Redis)
@api.get("/courses-cached")
def list_courses_cached(request, search: Optional[str] = None):
    """Endpoint dengan Redis caching - untuk optimasi performa"""
    cache_key = f"courses:list:{hashlib.md5((search or '').encode()).hexdigest()}"
    cached = cache.get(cache_key)
    
    if cached:
        return cached
    
    qs = Course.objects.all()
    if search:
        qs = qs.filter(name__icontains=search)
    
    result = {
        "count": qs.count(),
        "results": [CourseOut.from_orm(c) for c in qs],
    }
    
    cache.set(cache_key, result, 300)  # Cache 5 menit
    
    # Log ke MongoDB
    user_id = request.auth.id if hasattr(request, 'auth') and request.auth else None
    log_activity(user_id, 'list_cached', 'course', None)
    
    return result


# 2. Async Enrollment (Celery - Send Email)
@api.post("/enrollments-async", auth=auth)
def enroll_async(request, data: EnrollmentIn):
    """Enroll dengan pengiriman email async via Celery"""
    is_student(request.auth)
    
    course = get_object_or_404(Course, id=data.course_id)
    
    if CourseMember.objects.filter(course_id=course, user_id=request.auth).exists():
        raise HttpError(400, "Sudah enroll")
    
    member = CourseMember.objects.create(
        course_id=course,
        user_id=request.auth,
        roles="std",
    )
    
    # Kirim email via Celery (async)
    send_enrollment_email.delay(
        request.auth.id,
        course.id,
        request.auth.email,
        request.auth.username,
        course.name
    )
    
    # Log ke MongoDB
    log_activity(
        request.auth.id,
        'enroll_async',
        'course',
        course.id,
        {'course_name': course.name}
    )
    
    return {
        "message": "Enrolled successfully! Check your email for confirmation.",
        "enrollment": CourseMemberOut.from_orm(member)
    }


# 3. Complete Course & Generate Certificate (Celery)
@api.post("/courses/{id}/complete-async", auth=auth)
def complete_course_async(request, id: int):
    """Complete course dan generate certificate via Celery"""
    course = get_object_or_404(Course, id=id)
    
    # Cek apakah user terdaftar
    is_member = CourseMember.objects.filter(course_id=course, user_id=request.auth).exists()
    if not is_member:
        raise HttpError(403, "Not enrolled in this course")
    
    # Generate certificate via Celery
    generate_certificate.delay(
        request.auth.id,
        course.id,
        request.auth.username,
        course.name
    )
    
    # Record ke analytics MongoDB
    record_content_view(request.auth.id, course.id)
    
    # Log activity
    log_activity(
        request.auth.id,
        'complete_course',
        'course',
        course.id,
        {'course_name': course.name}
    )
    
    return {"message": "Course completed! Certificate is being generated."}


# 4. Export Course Report (Celery - Async)
@api.post("/courses/{id}/export-async", auth=auth)
def export_report_async(request, id: int):
    """Export report via Celery (async)"""
    course = get_object_or_404(Course, id=id)
    
    # Validasi hanya admin atau teacher pemilik course
    if not (is_admin_user(request.auth) or is_course_owner(request.auth, course)):
        raise HttpError(403, "Only course teacher or admin can export reports")
    
    export_course_report.delay(course.id, request.auth.email, course.name)
    
    return {"message": "Report is being generated. You will receive an email when ready."}


# 5. Popular Courses (MongoDB Aggregation)
@api.get("/analytics/popular-courses")
def popular_courses(request, limit: int = 5):
    """Get popular courses from MongoDB analytics"""
    popular = get_popular_courses(limit)
    return {"popular_courses": popular}


# 6. My Activity Logs (MongoDB)
@api.get("/analytics/my-activities", auth=auth)
def my_activities(request, limit: int = 20):
    """Get current user's activity log from MongoDB"""
    activities = get_user_activities(request.auth.id, limit)
    # Convert ObjectId to string for JSON serialization
    for act in activities:
        act['_id'] = str(act['_id'])
        act['timestamp'] = act['timestamp'].isoformat()
    return {"activities": activities}


# 7. Trigger Statistics Update (Admin Only)
@api.post("/admin/update-stats", auth=auth)
def trigger_stats(request):
    """Manual trigger untuk update course statistics via Celery"""
    is_admin(request.auth)
    update_course_statistics.delay()
    return {"message": "Statistics update task has been queued."}

# ================= WISHLIST =================

@api.post( "/courses/{id}/wishlist", auth=auth, response=WishlistOut, summary="Tambah Wishlist")
def add_wishlist(request, id: int):

    course = get_object_or_404(
        Course,
        id=id
    )

    wishlist, _ = CourseWishlist.objects.get_or_create(
        course=course,
        user=request.auth,
    )

    return wishlist


@api.delete("/courses/{id}/wishlist", auth=auth)
def remove_wishlist(request, id: int):

    CourseWishlist.objects.filter(
        course_id=id,
        user=request.auth,
    ).delete()

    return {"success": True}


@api.get( "/wishlist", auth=auth, response=List[WishlistOut])
def my_wishlist(request):

    return CourseWishlist.objects.filter(
        user=request.auth
    )

@api.get( "/courses/{id}/progress", auth=auth, response=CourseProgressOut)
def course_progress(request, id: int):

    course = get_object_or_404(
        Course,
        id=id
    )

    total_contents = CourseContent.objects.filter(
        course_id=course
    ).count()

    completed_contents = CourseContentCompletion.objects.filter(
        member_id__user_id=request.auth,
        content_id__course_id=course,
    ).count()

    percentage = 0

    if total_contents > 0:
        percentage = round(
            (completed_contents / total_contents) * 100,
            2
        )

    return {
        "course_id": course.id,
        "total_contents": total_contents,
        "completed_contents": completed_contents,
        "progress_percentage": percentage,
    }

# ================= DASHBOARD =================

@api.get("/dashboard", auth=auth, response=DashboardOut, summary="Dashboard Mahasiswa")
def dashboard(request):

    members = CourseMember.objects.filter(user_id=request.auth)
    active_courses = members.count()
    progress_list = []
    for member in members:

        total_contents = CourseContent.objects.filter(course_id=member.course_id).count()
        completed_contents = CourseContentCompletion.objects.filter(member_id=member).count()
        percentage = 0
        if total_contents > 0:
            percentage = round((completed_contents / total_contents) * 100, 2)

        progress_list.append({
            "course_id": member.course_id.id,
            "course_name": member.course_id.name,
            "progress_percentage": percentage,
        })

    enrolled_courses = members.values_list(
        "course_id",
        flat=True
    )

    recommended = Course.objects.exclude(
        id__in=enrolled_courses
    ).filter(
        status="published"
    ).order_by(
        "-created_at"
    )[:5]

    return {
        "active_courses": active_courses,
        "my_course_progress": progress_list,
        "recommended_courses": recommended,
    }