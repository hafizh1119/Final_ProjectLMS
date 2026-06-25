Nama    : Hafizh Naufal Nuha Kusuma

NIM     : A11.2023.14904

Kelas   : A11.4618

Repo    : https://github.com/hafizh1119/Final_ProjectLMS

# Deskripsi Project

**Simple-LMS** merupakan aplikasi Learning Management System (LMS) berbasis Django yang mendukung proses pembelajaran daring dengan tiga peran pengguna, yaitu Admin, Instructor, dan Student. Aplikasi ini menggunakan Docker Compose sebagai lingkungan deployment, PostgreSQL sebagai database, serta JWT Authentication untuk proses autentikasi pengguna. Sistem menyediakan fitur pengelolaan course, lesson (module & content), enrollment, dan progress belajar, serta dilengkapi dengan pencarian, filter, dan sorting course, review dan wishlist course, curriculum berbasis module dan content dengan perhitungan progress yang lebih akurat, serta student dashboard yang menampilkan ringkasan course aktif, progress pembelajaran, dan rekomendasi course.

## Fitur Dasar yang Sudah Berjalan

* **Docker Compose** – Project dapat dijalankan menggunakan Docker Compose sehingga seluruh layanan dapat dijalankan dalam satu lingkungan container.
* **PostgreSQL & Migration** – Database menggunakan PostgreSQL dan seluruh migration berhasil dijalankan untuk membangun struktur database.
* **JWT Authentication** – Mendukung proses autentikasi menggunakan JSON Web Token (JWT), meliputi registrasi, login, refresh token, serta pengelolaan profil pengguna.
* **Role Management** – Sistem menerapkan tiga peran pengguna, yaitu **Admin**, **Instructor**, dan **Student**, dengan hak akses yang berbeda sesuai fungsinya.
* **Course, Lesson, Enrollment, dan Progress** – Menyediakan endpoint untuk mengelola course, curriculum (module & content), enrollment mahasiswa, serta pelacakan progress pembelajaran.
* **Swagger/OpenAPI** – Seluruh endpoint REST API terdokumentasi dan dapat diuji secara langsung melalui halaman Swagger/OpenAPI.

## Fitur Tambahan yang Dipilih

| No |Fitur                                                                                                                                    | Kategori           | Poin |    Status   |
| -- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | :--: | :---------: |
| 1  | Search, filter, dan sorting course berdasarkan **keyword, category, instructor, level, status,** dan **sorting**                         | Course Discovery   |  12  | **Selesai** |
| 2  | Rating, review, dan wishlist course sehingga **Student** dapat memberikan review dan menyimpan course favorit                            | Student Engagement |  12  | **Selesai** |
| 3  | Curriculum berbasis **module** dan **content** serta perhitungan **progress belajar** yang lebih akurat berdasarkan penyelesaian content | Learning Progress  |  15  | **Selesai** |
| 4  | Student Dashboard yang menampilkan **ringkasan course aktif**, **progress pembelajaran**, dan **rekomendasi course**                     | Dashboard          |  12  | **Selesai** |

## Penjelasan Implementasi

### 1. Search, Filter, dan Sorting Course

Fitur ini memungkinkan pengguna mencari course berdasarkan **keyword**, serta melakukan filter berdasarkan **category**, **instructor**, **level**, dan **status**. Selain itu, sistem menyediakan fitur sorting untuk memudahkan pengguna menemukan course sesuai kebutuhan.

### 2. Rating, Review, dan Wishlist Course

Mahasiswa (Student) dapat memberikan rating dan review terhadap course yang telah diikuti, serta menyimpan course ke dalam wishlist sebagai daftar course favorit.

Sistem rating menggunakan skala 1–5, dengan keterangan:

1 = Sangat Buruk
2 = Buruk
3 = Cukup
4 = Baik
5 = Sangat Baik

Setiap mahasiswa hanya dapat memberikan satu review untuk setiap course yang diikuti, sehingga penilaian yang diberikan tetap konsisten.

### 3. Curriculum dan Progress Belajar

Setiap **course** memiliki struktur **module** dan **content** sebagai curriculum pembelajaran. Progress belajar dihitung berdasarkan jumlah **content** yang telah diselesaikan oleh mahasiswa dibandingkan dengan total content pada course, sehingga persentase progress menjadi lebih akurat.

### 4. Student Dashboard

Dashboard mahasiswa menampilkan informasi ringkas mengenai **jumlah course aktif**, **progress pembelajaran pada setiap course**, serta **rekomendasi course** yang dapat diikuti, sehingga mahasiswa dapat memantau aktivitas belajarnya dengan lebih mudah.

## Cara Menjalankan Project

### 1. Clone Repository

Clone repository ke komputer lokal.

```bash
git clone <repository-url>
cd Simple-LMS---Advanced-Features-Integration
```

---

### 2. Jalankan Docker Compose

Build image Docker dan jalankan seluruh service.

```bash
docker compose up --build -d
```

Pastikan seluruh container berhasil berjalan.

```bash
docker ps
```

---

### 3. Jalankan Database Migration

Masuk ke container aplikasi kemudian jalankan migration.

```bash
docker exec -it lms-app python manage.py migrate
```

Migration akan membuat seluruh tabel yang diperlukan pada database PostgreSQL.

---

### 4. Membuat Superuser

Buat akun **Admin** untuk mengakses Django Admin dengan menjalankan perintah berikut.

```bash
docker exec -it lms-app python manage.py createsuperuser
```

Gunakan kredensial berikut:

| Username | Password      |
| -------- | ------------- |
| `admin`  | `password123` |


### 5. Menjalankan Seeder

Isi database dengan data awal (teacher, student, category, course, module, content, enrollment, review, wishlist, dan progress).

```bash
docker exec -it lms-app python manage.py seed_data
```

Seeder akan membuat data dummy sehingga seluruh fitur dapat langsung diuji melalui API.

---

### 6. Akses Swagger/OpenAPI

Setelah seluruh proses selesai, dokumentasi API dapat diakses melalui browser.

```
http://localhost:8000/api/docs
```

Seluruh endpoint REST API dapat langsung diuji melalui halaman Swagger/OpenAPI.

---

### 7. Login Menggunakan Akun Seeder

Gunakan salah satu akun yang dibuat oleh seeder atau akun superuser untuk mencoba seluruh fitur sesuai hak akses **Admin**, **Instructor**, maupun **Student**.

## Akun Demo

Seeder akan membuat akun demo dengan kredensial berikut.

| Role       | Username                                                             | Password                                               |
| ---------- | -------------------------------------------------------------------- | ------------------------------------------------------ |
| Admin      | `admin` *(akun superuser yang dibuat dengan `createsuperuser`)*      | `password123`                                          |
| Instructor | `dosen01` – `dosen20`                                                | `password123`                                          |
| Student    | `mhs001` – `mhs080`                                                  | `password123`                                          |

> **Catatan:** Akun **Admin** dibuat menggunakan perintah `python manage.py createsuperuser`, sedangkan akun **Instructor** dan **Student** otomatis dibuat melalui perintah `python manage.py seed_data`.

## Endpoint Penting

Berikut merupakan endpoint utama yang digunakan untuk menguji seluruh fitur pada project **Simple-LMS**.

| Method     | Endpoint                         | Deskripsi                                                                                                |
| ---------- | -------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **POST**   | `/api/auth/register`             | Registrasi pengguna baru.                                                                                |
| **POST**   | `/api/auth/login`                | Login dan mendapatkan JWT Access Token serta Refresh Token.                                              |
| **GET**    | `/api/auth/me`                   | Menampilkan informasi pengguna yang sedang login.                                                        |
| **GET**    | `/api/courses`                   | Menampilkan daftar course beserta fitur search, filter, dan sorting.                                     |
| **POST**   | `/api/courses`                   | Menambahkan course baru.                                                                                 |
| **GET**    | `/api/courses/{id}`              | Menampilkan detail course.                                                                               |
| **GET**    | `/api/modules`                   | Menampilkan curriculum course berupa module beserta content.                                             |
| **POST**   | `/api/modules`                   | Menambahkan module pada course.                                                                          |
| **POST**   | `/api/enrollments`               | Melakukan enrollment (mendaftar) ke course.                                                              |
| **GET**    | `/api/enrollments/my-courses`    | Menampilkan daftar course yang telah diikuti oleh student.                                               |
| **POST**   | `/api/enrollments/{id}/progress` | Menandai content sebagai selesai dipelajari.                                                             |
| **GET**    | `/api/courses/{id}/progress`     | Menampilkan progress belajar pada suatu course.                                                          |
| **POST**   | `/api/courses/{id}/reviews`      | Memberikan rating dan review pada course.                                                                |
| **GET**    | `/api/courses/{id}/reviews`      | Menampilkan daftar review suatu course.                                                                  |
| **POST**   | `/api/courses/{id}/wishlist`     | Menambahkan course ke wishlist.                                                                          |
| **DELETE** | `/api/courses/{id}/wishlist`     | Menghapus course dari wishlist.                                                                          |
| **GET**    | `/api/wishlist`                  | Menampilkan daftar course favorit (wishlist).                                                            |
| **GET**    | `/api/dashboard`                 | Menampilkan dashboard mahasiswa yang berisi course aktif, progress pembelajaran, dan rekomendasi course. |

