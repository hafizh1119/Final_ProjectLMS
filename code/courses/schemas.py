from ninja import Schema, Field
from typing import Optional, List
from datetime import datetime


class RegisterIn(Schema):
    username: str
    email: str
    password: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    role: Optional[str] = "student"


class LoginIn(Schema):
    username: str
    password: str


class RefreshIn(Schema):
    refresh: str


class TokenOut(Schema):
    access: str
    refresh: str


class UserOut(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str

class InstructorOut(Schema):
    id: int
    username: str
    full_name: str


class ProfileUpdateIn(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class CourseIn(Schema):
    name: str
    description: Optional[str] = "-"
    price: Optional[int] = 10000

    category_id: Optional[int] = None

    level: Optional[str] = "beginner"
    status: Optional[str] = "published"


class CoursePatchIn(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None

    category_id: Optional[int] = None

    level: Optional[str] = None
    status: Optional[str] = None

class CategoryIn(Schema):
    name: str
    description: Optional[str] = ""


class CategoryOut(Schema):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class ModuleIn(Schema):
    title: str
    description: Optional[str] = ""
    order: Optional[int] = 1
    course_id: int

class ModuleContentOut(Schema):
    id: int
    name: str
    class Config: from_attributes = True

class ModuleCourseOut(Schema):
    id: int
    name: str

    class Config: from_attributes = True

class ModuleOut(Schema):
    id: int

    course: ModuleCourseOut

    title: str
    description: str
    order: int

    contents: List[ModuleContentOut]

    class Config:
        from_attributes = True

    @staticmethod
    def resolve_course(obj):
        return obj.course

    @staticmethod
    def resolve_contents(obj):
        return obj.contents.all()


class CourseOut(Schema):
    id: int
    name: str
    description: str
    price: int

    category_id: Optional[int] = None
    teacher_id: int

    level: str
    status: str

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CourseListOut(Schema):
    count: int
    results: List[CourseOut]

class CourseFilterIn(Schema):
    search: Optional[str] = None
    category: Optional[int] = None
    teacher: Optional[int] = None
    level: Optional[str] = None
    status: Optional[str] = None
    sort: Optional[str] = None


class EnrollmentIn(Schema):
    course_id: int


class ProgressIn(Schema):
    content_id: int


class ReviewIn(Schema):
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="""
Nilai rating course:
1 = Sangat Buruk
2 = Buruk
3 = Cukup
4 = Baik
5 = Sangat Baik
"""
    )

    review: Optional[str] = Field(
        "",
        description="Komentar atau ulasan terhadap course."
    )


class ReviewOut(Schema):
    id: int
    course_id: int
    user_id: int
    rating: int
    review: str
    created_at: datetime

    class Config:
        from_attributes = True

    @staticmethod
    def resolve_course_id(obj):
        return obj.course.id

    @staticmethod
    def resolve_user_id(obj):
        return obj.user.id
    

class WishlistOut(Schema):
    id: int
    course_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

    @staticmethod
    def resolve_course_id(obj):
        return obj.course.id

    @staticmethod
    def resolve_user_id(obj):
        return obj.user.id
    

class CourseMemberOut(Schema):
    id: int
    course_id: CourseOut
    user_id: int
    roles: str

    class Config:
        from_attributes = True

    @staticmethod
    def resolve_user_id(obj):
        return obj.user_id.id


class CourseContentCompletionOut(Schema):
    id: int
    member_id: int      
    content_id: int    
    completed: bool
    completed_at: datetime

    class Config:
        from_attributes = True

    @staticmethod
    def resolve_member_id(obj):
        return obj.member_id_id  

    @staticmethod
    def resolve_content_id(obj):
        return obj.content_id_id

class DashboardCourseProgressOut(Schema):
    course_id: int
    course_name: str
    progress_percentage: float

class DashboardOut(Schema):
    active_courses: int

    my_course_progress: List[DashboardCourseProgressOut] = Field(
        default_factory=list
    )

    recommended_courses: List[CourseOut] = Field(
        default_factory=list
    )


class CourseProgressOut(Schema):
    course_id: int
    total_contents: int
    completed_contents: int
    progress_percentage: float