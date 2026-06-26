# Simple-LMS - Advanced Features Integration

## Deskripsi Project

**Simple-LMS** merupakan aplikasi **Learning Management System (LMS)** berbasis **Django** yang mendukung proses pembelajaran daring dengan tiga peran pengguna, yaitu **Admin**, **Instructor**, dan **Student**. Aplikasi ini menggunakan **Docker Compose** sebagai lingkungan deployment, **PostgreSQL** sebagai database, serta **JWT Authentication** untuk proses autentikasi pengguna.

Project mengimplementasikan pengelolaan **course**, **lesson (module & content)**, **enrollment**, **progress pembelajaran**, serta fitur tambahan berupa **search, filter, dan sorting course**, **rating, review, wishlist**, **curriculum berbasis module dan lesson**, serta **student dashboard**.

---

## Teknologi yang Digunakan

* Python 3.11
* Django 5
* Django Ninja
* PostgreSQL
* Docker & Docker Compose
* MongoDB
* JWT Authentication

---

## Cara Menjalankan Project

### 1. Clone Repository

```bash
git clone https://github.com/hafizh1119/Final_ProjectLMS.git
cd Final_ProjectLMS
```

### 2. Jalankan Docker Compose

```bash
docker compose up --build -d
```

Pastikan seluruh container berjalan.

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

Gunakan akun berikut:

| Username | Password    |
| -------- | ----------- |
| admin    | password123 |

### 5. Jalankan Seeder

```bash
docker exec -it lms-app python manage.py seed_data
```

### 6. Buka Swagger

```
http://localhost:8000/api/docs
```

---

## Akun Demo

| Role       | Username              | Password      |
| ---------- | --------------------- | ------------- |
| Admin      | `admin`               | `password123` |
| Instructor | `dosen01` – `dosen20` | `password123` |
| Student    | `mhs001` – `mhs080`   | `password123` |

---

## Dokumentasi Lengkap

Dokumentasi implementasi, pengujian, serta screenshot hasil testing dapat dilihat pada file berikut:

* **[FINAL_PROJECT_REPORT.md](FINAL_PROJECT_REPORT.md)**

Dokumentasi tersebut mencakup:

* Deskripsi Project
* Fitur Dasar
* Fitur Tambahan
* Penjelasan Implementasi
* Cara Menjalankan Project
* Endpoint Penting
* Pengujian Docker Compose
* Pengujian Migration
* Pengujian Seeder
* Pengujian Authentication JWT
* Pengujian Role Management
* Pengujian Course
* Pengujian Lesson
* Pengujian Enrollment
* Pengujian Progress
* Pengujian Search, Filter, dan Sorting
* Pengujian Rating, Review, dan Wishlist
* Pengujian Student Dashboard

---

## Author

**Hafizh Naufal Nuha Kusuma**
NIM : A11.2023.14904
