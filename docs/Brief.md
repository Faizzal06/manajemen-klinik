# Brief Proposal Tugas Besar PBO

## Sistem Manajemen Klinik

**Platform:** Python, Streamlit, SQLite\
**Jumlah anggota:** 4 orang\
**Jenis aplikasi:** Web application responsif

------------------------------------------------------------------------

## 1. Gambaran Umum

Sistem Manajemen Klinik merupakan aplikasi untuk membantu proses
administrasi klinik secara terkomputerisasi. Sistem dirancang untuk
mengelola data pasien, data dokter, janji pemeriksaan, serta catatan dan
riwayat kunjungan pasien.

Aplikasi dibuat menggunakan Python dengan pendekatan Pemrograman
Berorientasi Objek (PBO). Streamlit digunakan sebagai antarmuka agar
aplikasi dapat diakses melalui browser desktop maupun perangkat mobile,
sedangkan SQLite digunakan untuk menyimpan data.

Sistem menerapkan autentikasi dan otorisasi berbasis peran. Terdapat tiga
role utama, yaitu **Admin/Petugas**, **Dokter**, dan **Pasien**. Setiap
role hanya dapat mengakses menu dan tindakan sesuai haknya. Pasien dapat
mendaftar akun sendiri, masuk ke dashboard, lalu membuat janji temu
secara mandiri tanpa harus menghubungi petugas. Password pengguna tidak
disimpan dalam bentuk teks biasa, melainkan sebagai hash dengan salt.

------------------------------------------------------------------------

## 2. Tujuan

1.  Mempermudah pengelolaan data pasien dan dokter.
2.  Membantu pencatatan serta pengelolaan janji pemeriksaan.
3.  Menyimpan informasi pemeriksaan dan riwayat kunjungan pasien.
4.  Menerapkan konsep Encapsulation, Inheritance, dan Polymorphism.
5.  Menerapkan pengujian unit menggunakan `unittest`.
6.  Menerapkan autentikasi dan otorisasi berbasis role untuk admin,
    dokter, dan pasien.
7.  Memberikan kemandirian kepada pasien untuk mendaftar dan membuat
    janji temu melalui dashboard.

------------------------------------------------------------------------

## 3. Ruang Lingkup Fitur

| Fitur | Deskripsi |
|---|---|
| Autentikasi & Hak Akses | Login, logout, dan pembatasan menu/aksi berdasarkan role Admin/Petugas, Dokter, dan Pasien. |
| Registrasi Pasien | Pasien membuat akun sendiri; sistem otomatis membuat nomor rekam medis (`no_rm`) dan menghubungkan akun dengan data pasien. |
| Dashboard | Menampilkan ringkasan sesuai role: ringkasan klinik untuk admin, jadwal hari ini untuk dokter, serta ringkasan dan pintasan booking untuk pasien. |
| Manajemen Pasien | Admin menambah, melihat, mengubah, menghapus, dan mencari data pasien. |
| Manajemen Dokter | Admin mengelola data dokter, spesialisasi, jadwal praktik, serta membuat akun login dokter. |
| Janji Pemeriksaan | Admin melihat/membuat/membatalkan seluruh janji; pasien membuat dan membatalkan janji miliknya sendiri. |
| Pemeriksaan | Dokter atau admin mencatat keluhan, diagnosis, tindakan, dan status pemeriksaan. |
| Riwayat Kunjungan | Admin melihat seluruh riwayat; dokter melihat riwayat pasien yang ditanganinya; pasien melihat riwayatnya sendiri. |
| Manajemen Akun | Admin melihat daftar akun, melakukan reset password, serta mengaktifkan/menonaktifkan akun. |
| Akun Saya | Semua role dapat melihat profil singkat dan mengganti password sendiri. |

### 3.1 Role dan Hak Akses

| Kemampuan | Admin/Petugas | Dokter | Pasien |
|---|---|---|---|
| Login dan logout | Ya | Ya | Ya |
| Registrasi akun mandiri | - | - | Ya |
| Melihat dashboard | Ya | Ya | Ya |
| Mengelola data pasien | Ya | - | - |
| Mengelola data dokter | Ya | - | - |
| Membuat akun dokter | Ya | - | - |
| Melihat seluruh janji | Ya | - | - |
| Melihat janji milik sendiri | - | Ya | Ya |
| Membuat janji untuk pasien lain | Ya | - | - |
| Membuat janji untuk diri sendiri | - | - | Ya |
| Membatalkan janji | Semua janji | Janji sendiri | Janji sendiri |
| Mengisi hasil pemeriksaan | Ya | Janji sendiri | - |
| Melihat seluruh riwayat | Ya | - | - |
| Melihat riwayat pasien yang ditangani | - | Ya | - |
| Melihat riwayat sendiri | - | - | Ya |
| Mengelola akun pengguna | Ya | - | - |
| Mengganti password sendiri | Ya | Ya | Ya |

### 3.2 Alur Utama Login dan Booking Pasien

1.  Saat aplikasi pertama kali dijalankan, sistem membuat tabel database
    dan akun admin default jika belum ada.
2.  Pasien membuka halaman login, memilih tab **Daftar Pasien**, lalu
    mengisi data diri serta username dan password.
3.  Sistem membuat `no_rm` otomatis, menyimpan data pasien, dan membuat
    akun yang terhubung ke data pasien tersebut.
4.  Pasien login dan masuk ke dashboard pasien.
5.  Pada tab **Buat Janji Temu**, pasien memilih dokter, tanggal, slot
    waktu, dan mengisi keluhan. Sistem menampilkan jadwal praktik dokter
    dan mencegah bentrok jadwal.
6.  Setelah janji dibuat, pasien dapat melihatnya pada tab **Janji Saya**
    dan membatalkan janji yang masih berstatus `Terjadwal`.
7.  Dokter login, melihat janji miliknya, lalu mengisi diagnosis dan
    tindakan. Status janji berubah menjadi `Selesai`.
8.  Pasien dapat melihat diagnosis, tindakan, dan riwayat kunjungannya
    pada tab **Riwayat Saya**.

------------------------------------------------------------------------

## 4. Teknologi

-   **Python:** bahasa pemrograman utama.
-   **Streamlit:** antarmuka web responsif dan pengelolaan sesi login
    melalui `st.session_state`.
-   **SQLite:** basis data relasional lokal.
-   **`unittest`:** pengujian unit bawaan Python.
-   **`hashlib` dan `secrets`:** pembuatan hash password PBKDF2-HMAC-SHA256
    dengan salt acak. Keduanya merupakan pustaka standar Python sehingga
    tidak menambah dependency baru.
-   **`requirements.txt`:** tetap hanya berisi `streamlit`.

**Catatan akses mobile:** Streamlit bukan aplikasi Android native.
Aplikasi dibuka melalui browser. Untuk pengujian melalui ponsel dalam
jaringan Wi-Fi yang sama, server Streamlit perlu dijalankan agar dapat
diakses dari jaringan lokal. Akses melalui internet memerlukan
deployment/hosting.

------------------------------------------------------------------------

## 5. Rancangan Class Utama

Pembagian berikut merupakan rancangan awal untuk kelompok beranggotakan
empat orang. Setiap anggota bertanggung jawab atas satu class utama,
termasuk implementasi, pengujian, dan dokumentasinya.

| Anggota | Class | Tanggung jawab |
|---|---|---|
| 1 | `Person` | Class induk yang menyimpan informasi umum seseorang. |
| 2 | `Patient` | Mengelola data dan informasi pasien. |
| 3 | `Doctor` | Mengelola data dokter, spesialisasi, dan jadwal praktik. |
| 4 | `Appointment` | Mengelola janji dan catatan pemeriksaan. |

### Ringkasan Class

-   **`Person`**: atribut umum seperti ID, nama, alamat, dan nomor
    telepon; menyediakan informasi dasar seseorang.
-   **`Patient(Person)`**: mewarisi `Person`, dengan atribut tambahan
    seperti nomor rekam medis, tanggal lahir, dan jenis kelamin.
-   **`Doctor(Person)`**: mewarisi `Person`, dengan atribut tambahan
    seperti ID dokter, spesialisasi, dan jadwal praktik.
-   **`Appointment`**: menghubungkan objek pasien dan dokter, serta
    menyimpan tanggal, waktu, keluhan, diagnosis, tindakan, dan status
    pemeriksaan.

### Class Pendukung Autentikasi

Autentikasi tidak disimpan di dalam `Patient` atau `Doctor` agar data
medis dan data akun tetap terpisah. Class pendukung yang ditambahkan:

-   **`Account`** (abstract): menyimpan ID akun, username, nama tampilan,
    dan status aktif. Atribut bersifat private dan diakses melalui
    `@property`.
-   **`AdminAccount(Account)`**: akun admin/petugas dengan akses
    pengelolaan data dan akun.
-   **`DoctorAccount(Account)`**: akun dokter yang terhubung ke
    `doctor_id`.
-   **`PatientAccount(Account)`**: akun pasien yang terhubung ke
    `patient_id`.
-   **`AccountRepository`**: operasi database untuk tabel `users`.
-   **`AuthService`**: logika login, registrasi, seed admin, pembuatan
    akun dokter, ganti/reset password, dan aktivasi akun.

Setiap subclass `Account` mengimplementasikan method seperti
`get_role_label()`, `get_menu_items()`, dan hak akses (`can_manage_patients()`,
`can_manage_doctors()`, `can_examine()`, `can_book_for_self()`).

### Diagram UML

Diagram UML lengkap (class diagram, custom exception, ER diagram, dan alur
login/booking) tersedia di [`UML.md`](UML.md).

------------------------------------------------------------------------

## 6. Penerapan Konsep PBO

1.  **Encapsulation:** atribut penting dibuat terlindungi (misalnya
    menggunakan atribut private) dan diakses melalui method atau
    `@property`. Data akun juga tidak menyimpan password secara langsung.
2.  **Inheritance:** `Patient` dan `Doctor` mewarisi atribut serta
    perilaku umum dari `Person`.
3.  **Polymorphism:** `Patient` dan `Doctor` dapat mengimplementasikan
    ulang method seperti `get_info()` atau `get_role()` sesuai
    karakteristik masing-masing.
4.  **Inheritance tambahan:** `AdminAccount`, `DoctorAccount`, dan
    `PatientAccount` mewarisi class abstrak `Account`.
5.  **Polymorphism tambahan:** setiap jenis akun mengimplementasikan
    `get_role_label()`, daftar menu, dan hak akses dengan perilaku
    berbeda. Navigasi aplikasi dibangun dari hasil polymorphism ini.
6.  **Custom Exception:** membuat exception khusus, antara lain
    `AppointmentConflictError`, `PatientNotFoundError`,
    `DoctorNotFoundError`, `UsernameAlreadyExistsError`,
    `AuthenticationError`, `AccountNotFoundError`,
    `InvalidAccountDataError`, dan `UnauthorizedActionError`.

------------------------------------------------------------------------

## 7. Rancangan Basis Data

Tabel utama yang direncanakan:

| Tabel | Kolom penting |
|---|---|
| `patients` | `id`, `no_rm`, `nama`, `alamat`, `no_telepon`, `tanggal_lahir`, `jenis_kelamin` |
| `doctors` | `id`, `nama`, `alamat`, `no_telepon`, `spesialisasi`, `jadwal_praktik` |
| `appointments` | `id`, `patient_id`, `doctor_id`, `tanggal`, `waktu`, `keluhan`, `diagnosis`, `tindakan`, `status` |
| `users` | `id`, `username`, `password_hash`, `role`, `patient_id`, `doctor_id`, `is_active`, `created_at` |

Relasi:

-   Satu pasien dapat memiliki banyak janji pemeriksaan.
-   Satu dokter dapat menangani banyak janji pemeriksaan.
-   `appointments.patient_id` menjadi foreign key ke `patients.id`.
-   `appointments.doctor_id` menjadi foreign key ke `doctors.id`.
-   Satu akun pasien terhubung ke satu data pasien melalui
    `users.patient_id` (unik).
-   Satu akun dokter terhubung ke satu data dokter melalui
    `users.doctor_id` (unik).
-   Akun admin tidak memiliki `patient_id` maupun `doctor_id`.
-   Foreign key akun memakai `ON DELETE CASCADE`, sehingga akun ikut
    terhapus saat data pasien/dokter dihapus.

Nomor rekam medis (`no_rm`) direncanakan unik. Validasi juga diperlukan
untuk memastikan pasien dan dokter tersedia serta mencegah bentrok
jadwal dokter.

### 7.1 Tabel `users`

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL COLLATE NOCASE UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'dokter', 'pasien')),
    patient_id INTEGER UNIQUE REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id  INTEGER UNIQUE REFERENCES doctors(id)  ON DELETE CASCADE,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (role = 'admin'  AND patient_id IS NULL     AND doctor_id IS NULL) OR
        (role = 'pasien' AND patient_id IS NOT NULL AND doctor_id IS NULL) OR
        (role = 'dokter' AND doctor_id IS NOT NULL  AND patient_id IS NULL)
    )
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
```

### 7.2 Aturan Data Autentikasi

-   `username` unik dan tidak membedakan huruf besar/kecil
    (`COLLATE NOCASE`), dengan panjang 3–30 karakter.
-   Password minimal 8 karakter dan disimpan sebagai hash
    PBKDF2-HMAC-SHA256 dengan salt acak.
-   Akun dengan `is_active = 0` tidak dapat login.
-   Akun admin default dibuat otomatis saat aplikasi pertama kali
    dijalankan. Password default wajib diganti sebelum presentasi.
-   Registrasi pasien membuat `no_rm` otomatis dengan format
    `RM-0001`, `RM-0002`, dan seterusnya.
-   Data pasien dan akun dibuat dalam satu transaksi agar tidak ada
    pasien tanpa akun jika proses gagal.
-   File `data/clinic.db` tidak di-commit ke repository.

------------------------------------------------------------------------

## 8. Rancangan Antarmuka

### 8.1 Halaman Login dan Registrasi

Halaman awal aplikasi menampilkan dua tab:

1.  **Masuk**: form username dan password. Jika berhasil, pengguna
    diarahkan ke dashboard sesuai role. Jika gagal, tampil pesan generik
    "Username atau password salah".
2.  **Daftar Pasien**: form username, password, konfirmasi password,
    nama, alamat, nomor telepon, tanggal lahir, dan jenis kelamin.
    Setelah berhasil, akun langsung terhubung ke data pasien baru.

Setelah login, sidebar menampilkan nama pengguna, role, menu sesuai hak
akses, dan tombol **Logout**.

### 8.2 Navigasi per Role

| Admin/Petugas | Dokter | Pasien |
|---|---|---|
| Dashboard | Dashboard | Dashboard |
| Manajemen Pasien | Janji Saya | Akun Saya |
| Manajemen Dokter | Pemeriksaan | |
| Janji & Pemeriksaan | Riwayat Pasien | |
| Riwayat Kunjungan | Akun Saya | |
| Manajemen Akun | | |
| Akun Saya | | |

### 8.3 Dashboard Pasien

Dashboard pasien menampilkan ringkasan jumlah janji aktif, jumlah
kunjungan selesai, dan jumlah dokter yang tersedia. Di bawahnya terdapat
tiga tab:

1.  **Buat Janji Temu**: pilih dokter (menampilkan spesialisasi dan
    jadwal praktik), tanggal, slot waktu, dan keluhan. Slot waktu yang
    sudah terisi tidak ditampilkan. Sistem tetap memvalidasi bentrok saat
    tombol simpan ditekan.
2.  **Janji Saya**: daftar janji milik pasien beserta status. Pasien dapat
    membatalkan janji yang masih `Terjadwal` dan belum lewat.
3.  **Riwayat Saya**: daftar kunjungan dengan diagnosis dan tindakan.
    Pasien tidak dapat melihat atau mengubah data pasien lain.

### 8.4 Dashboard Dokter

Dashboard dokter menampilkan janji pada hari tersebut, jumlah janji yang
menunggu pemeriksaan, dan jumlah pemeriksaan selesai. Dokter dapat
melihat janji miliknya, mengisi diagnosis serta tindakan, dan melihat
riwayat pasien yang pernah ditanganinya.

### 8.5 Halaman Admin

Admin dapat mengelola data pasien, data dokter, seluruh janji, hasil
pemeriksaan, dan riwayat kunjungan. Pada halaman Manajemen Dokter
tersedia form untuk membuat akun login dokter. Halaman Manajemen Akun
menampilkan daftar akun, reset password, serta aktivasi/nonaktivasi akun.
Admin tidak dapat menonaktifkan akunnya sendiri atau admin aktif terakhir.

### 8.6 Catatan Responsif

Antarmuka dirancang sederhana dan responsif. Formulir diupayakan tetap
nyaman digunakan pada layar ponsel, sementara tabel data perlu disajikan
agar tetap mudah dibaca pada layar kecil. Form menggunakan kolom yang
akan turun menjadi satu kolom pada layar sempit, dan tabel menggunakan
lebar penuh.

------------------------------------------------------------------------

## 9. Struktur Folder Awal

``` text
ClinicManagementSystem/
├── main.py
├── config.py
├── auth/
│   ├── __init__.py
│   ├── security.py
│   ├── service.py
│   └── session.py
├── models/
│   ├── __init__.py
│   ├── person.py
│   ├── patient.py
│   ├── doctor.py
│   ├── appointment.py
│   └── account.py
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── schema.py
│   ├── operations.py
│   └── accounts.py
├── exceptions/
│   ├── __init__.py
│   └── clinic_exceptions.py
├── ui/
│   ├── __init__.py
│   ├── login.py
│   ├── dashboard.py
│   ├── patients.py
│   ├── doctors.py
│   ├── appointments.py
│   ├── history.py
│   ├── patient_portal.py
│   ├── doctor_portal.py
│   ├── account.py
│   └── accounts_admin.py
├── tests/
│   ├── __init__.py
│   ├── test_person.py
│   ├── test_patient.py
│   ├── test_doctor.py
│   ├── test_appointment.py
│   ├── test_account.py
│   ├── test_auth.py
│   └── test_repository.py
├── data/
│   └── clinic.db
├── docs/
│   └── Brief.md
├── requirements.txt
├── .gitignore
└── README.md
```

Keterangan: file `auth/`, `models/account.py`, `database/accounts.py`,
halaman portal, dan file test baru merupakan bagian dari fitur
autentikasi dan booking mandiri pasien.

------------------------------------------------------------------------

## 10. Pembagian Pekerjaan Awal

Pembagian class utama mengikuti tabel pada bagian 5. Untuk pekerjaan
antarmuka dan integrasi, pembagian dapat dilakukan sebagai berikut:

| Anggota | Class utama | Pekerjaan antarmuka dan integrasi |
|---|---|---|
| 1 | `Person` | Kerangka aplikasi, `Account` dan layer autentikasi (`auth/`), session, navigasi per role, halaman login, serta koordinasi integrasi. |
| 2 | `Patient` | Halaman Manajemen Pasien, form registrasi pasien, dashboard pasien bagian data diri, janji, dan riwayat. |
| 3 | `Doctor` | Halaman Manajemen Dokter, pembuatan akun dokter, dashboard dokter, dan halaman riwayat pasien. |
| 4 | `Appointment` | Logika booking dan bentrok jadwal, pembatalan, pemeriksaan, halaman janji admin, serta integrasi dashboard pasien bagian booking. |

Seluruh anggota tetap perlu berkoordinasi untuk integrasi database,
pengujian aplikasi, dokumentasi, dan penyelesaian laporan. Fitur booking
pasien melibatkan Anggota 2 (antarmuka), Anggota 4 (logika janji), dan
Anggota 1 (integrasi akun).

------------------------------------------------------------------------

## 11. Rencana Pengerjaan

| Tahap | Target |
|---|---|
| Pertemuan 11 | Menentukan tema, anggota, pembagian class, rancangan UML, dan rancangan awal. |
| Pertemuan 12 | Membuat skeleton code class, atribut, method, struktur proyek, skema database termasuk tabel `users`, serta placeholder halaman login/portal dan test. |
| Pertemuan 13 | Mengimplementasikan class, Custom Exception, autentikasi, CRUD, dan unit test awal termasuk login serta bentrok jadwal. |
| Pertemuan 14 | Mengintegrasikan antarmuka, class, database, menu per role, portal pasien, portal dokter, manajemen akun, serta menyelesaikan pengujian dan dokumentasi. |
| Pertemuan 15 | Menyerahkan source code ZIP, laporan PDF beserta logbook, dan video presentasi. |

------------------------------------------------------------------------

## 12. Menjalankan Aplikasi

Isi awal `requirements.txt`:

``` text
streamlit
```

Instal dependensi dan jalankan aplikasi:

``` bash
pip install -r requirements.txt
streamlit run main.py
```

Saat pertama kali dijalankan, aplikasi membuat database
`data/clinic.db` dan akun admin default:

``` text
Username: admin
Password: admin123
```

Password default tersebut **wajib diganti** sebelum presentasi. Pada
tahap skeleton, halaman login dan portal masih berupa placeholder dengan
komentar TODO; implementasi penuh dilakukan pada Pertemuan 13–14.

Menjalankan unit test:

``` bash
python -m unittest discover -s tests -v
```

Untuk mengakses aplikasi dari perangkat lain dalam jaringan lokal yang
sama:

``` bash
streamlit run main.py --server.address 0.0.0.0
```

Catatan: file `data/clinic.db` dibuat otomatis dan tidak di-commit ke
repository. Folder `__pycache__`, file `.pyc`, virtual environment, dan
database lokal sudah dicantumkan pada `.gitignore`.

------------------------------------------------------------------------

## 13. Pengujian Autentikasi dan Booking

| File test | Fokus pengujian |
|---|---|
| `test_person.py` | Encapsulation `Person`, validasi nama/telepon, dan sifat abstract class. |
| `test_patient.py` | Inheritance `Patient`, validasi `no_rm`, jenis kelamin, dan perhitungan umur. |
| `test_doctor.py` | Inheritance `Doctor`, validasi spesialisasi, dan pengecekan jadwal praktik. |
| `test_appointment.py` | Pembuatan janji, bentrok jadwal, pembatalan, dan penyelesaian pemeriksaan. |
| `test_account.py` | Inheritance dan polymorphism `AdminAccount`, `DoctorAccount`, `PatientAccount`, serta hak akses. |
| `test_auth.py` | Hash password, login berhasil/gagal, akun nonaktif, registrasi pasien, dan username duplikat. |
| `test_repository.py` | CRUD pasien/dokter/janji, pencarian, `no_rm` unik, dan slot waktu yang sudah terisi. |

Pengujian menggunakan database sementara agar tidak mengganggu data
aplikasi. Perintah menjalankan:

``` bash
python -m unittest discover -s tests -v
```

------------------------------------------------------------------------

## 14. Catatan Keamanan dan Batasan

-   Password tidak disimpan sebagai teks biasa. Sistem memakai
    PBKDF2-HMAC-SHA256 dengan salt acak dan perbandingan hash yang aman.
-   Pesan login gagal dibuat generik agar tidak membocorkan username yang
    terdaftar.
-   Setiap halaman dan aksi memeriksa role akun. Pasien hanya dapat
    melihat dan membatalkan janji miliknya sendiri; dokter hanya dapat
    memeriksa janji miliknya.
-   Akun admin default hanya untuk kemudahan demonstrasi dan harus
    diganti sebelum presentasi.
-   Login memakai `st.session_state`. Menutup browser atau tab berarti
    logout; belum ada fitur "remember me" berbasis cookie.
-   Registrasi mandiri selalu membuat data pasien baru. Fitur klaim rekam
    medis lama yang sudah dibuat admin belum termasuk dalam ruang
    lingkup.
-   Jadwal praktik dokter masih berupa teks bebas. Sistem menampilkan
    jadwal tersebut dan mencegah bentrok pada dokter, tanggal, dan jam
    yang sama, tetapi belum membatasi slot berdasarkan hari praktik.
-   Reset password dilakukan oleh admin. Belum ada reset melalui email
    atau OTP.
-   Aplikasi ini ditujukan untuk tugas besar dan demonstrasi lokal, bukan
    untuk penggunaan produksi.
