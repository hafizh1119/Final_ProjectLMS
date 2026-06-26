# Simple-LMS - Advanced Features Integration

Simple-LMS merupakan aplikasi **Learning Management System (LMS)** berbasis **Django** yang mendukung tiga peran pengguna (**Admin, Instructor, dan Student**). Project dijalankan menggunakan **Docker Compose**, menggunakan **PostgreSQL** sebagai database, serta menyediakan REST API yang terdokumentasi menggunakan **Swagger/OpenAPI**.

---

## Model Utama

Project ini menggunakan beberapa model utama sebagai berikut:

| Model                                  | Keterangan                                                                                                  |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **User**                               | Menyimpan data pengguna dengan peran **Admin**, **Instructor**, dan **Student**.                            |
| **Category**                           | Mengelompokkan course berdasarkan kategori tertentu.                                                        |
| **Course**                             | Menyimpan informasi utama mengenai mata kuliah yang tersedia.                                               |
| **CourseModule**                       | Merepresentasikan section atau module pada setiap course.                                                   |
| **CourseContent (Lesson)**             | Merepresentasikan lesson atau materi pembelajaran yang berada di dalam setiap module.                       |
| **CourseMember (Enrollment)**          | Menyimpan data mahasiswa yang telah melakukan enrollment pada course.                                       |
| **CourseContentCompletion (Progress)** | Menyimpan progress pembelajaran berdasarkan lesson (course content) yang telah diselesaikan oleh mahasiswa. |

## Model Tambahan

Project ini menambahkan beberapa model untuk mendukung fitur tambahan yang diimplementasikan.

| Model | Fungsi |
|-------|--------|
| **CourseModule** | Menyusun curriculum menjadi beberapa section/module pada setiap course. |
| **CourseContentCompletion** | Menyimpan progress penyelesaian lesson sehingga persentase belajar dapat dihitung secara akurat. |
| **CourseReview** | Menyimpan rating dan review yang diberikan mahasiswa terhadap course. |
| **CourseWishlist** | Menyimpan daftar course favorit (wishlist) milik mahasiswa. |

# Cara Menjalankan Project

### 1. Clone Repository

```bash
git clone https://github.com/hafizh1119/Final_ProjectLMS.git
cd Final_ProjectLMS
```

### 2. Jalankan Docker Compose

```bash
docker compose up --build -d
```

Pastikan seluruh container telah berjalan.

```bash
docker ps
```

### 3. Jalankan Migration

```bash
docker exec -it lms-app python manage.py migrate
```

### 4. Membuat Superuser

```bash
docker exec -it lms-app python manage.py createsuperuser
```

Gunakan akun berikut.

| Username | Password      |
| -------- | ------------- |
| `admin`  | `password123` |

### 5. Jalankan Seeder

```bash
docker exec -it lms-app python manage.py seed_data
```

### 6. Akses Swagger

```
http://localhost:8000/api/docs
```

---

# Akun Demo

| Role       | Username              | Password      |
| ---------- | --------------------- | ------------- |
| Admin      | `admin`               | `password123` |
| Instructor | `dosen01` – `dosen20` | `password123` |
| Student    | `mhs001` – `mhs080`   | `password123` |

---

# Endpoint Utama

## Authentication

* `POST /api/auth/register`
* `POST /api/auth/login`
* `POST /api/auth/refresh`
* `GET /api/auth/me`

## Course

* `GET /api/courses`
* `POST /api/courses`
* `GET /api/courses/{id}`

## Lesson

* `GET /api/lessons`
* `POST /api/lessons`

## Enrollment

* `POST /api/enrollments`
* `GET /api/enrollments/my-courses`

## Progress

* `POST /api/enrollments/{id}/progress`
* `GET /api/courses/{id}/progress`

## Review

* `POST /api/courses/{id}/reviews`
* `GET /api/courses/{id}/reviews`

## Wishlist

* `POST /api/courses/{id}/wishlist`
* `DELETE /api/courses/{id}/wishlist`
* `GET /api/wishlist`

## Dashboard

* `GET /api/dashboard`

---

# Dokumentasi Lengkap

Dokumentasi implementasi, pengujian, dan screenshot dapat dilihat pada file **FINAL_PROJECT_REPORT.md**.
