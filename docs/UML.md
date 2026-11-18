# Diagram UML — Sistem Manajemen Klinik

Dokumen ini berisi diagram UML dalam format **Mermaid**. Diagram dapat
dirender langsung di GitHub, GitLab, atau VS Code dengan ekstensi Mermaid.

Catatan: atribut dengan awalan `__` pada kode Python adalah atribut private
(name mangling). Pada diagram, visibility tetap ditulis sebagai private (`-`).

------------------------------------------------------------------------

## 1. Class Diagram — Model Domain

```mermaid
classDiagram
    class Person {
        <<abstract>>
        -__id : int
        -__nama : str
        -__alamat : str
        -__no_telepon : str
        +id : int
        +nama : str
        +alamat : str
        +no_telepon : str
        +get_role() str
        +get_info() str
    }

    class Patient {
        -__no_rm : str
        -__tanggal_lahir : str
        -__jenis_kelamin : str
        +no_rm : str
        +tanggal_lahir : str
        +jenis_kelamin : str
        +get_role() str
        +get_info() str
        +hitung_umur() int
    }

    class Doctor {
        -__spesialisasi : str
        -__jadwal_praktik : str
        +spesialisasi : str
        +jadwal_praktik : str
        +get_role() str
        +get_info() str
        +cek_ketersediaan(hari) bool
    }

    class Appointment {
        -__id : int
        -__patient : Patient
        -__doctor : Doctor
        -__tanggal : str
        -__waktu : str
        -__keluhan : str
        -__diagnosis : str
        -__tindakan : str
        -__status : str
        +id : int
        +patient : Patient
        +doctor : Doctor
        +tanggal : str
        +waktu : str
        +keluhan : str
        +diagnosis : str
        +tindakan : str
        +status : str
        +selesaikan_pemeriksaan(diagnosis, tindakan) void
        +batalkan_janji() void
    }

    Person <|-- Patient
    Person <|-- Doctor
    Patient "1" -- "0..*" Appointment : memiliki
    Doctor "1" -- "0..*" Appointment : menangani
```

Keterangan:

- `Person` adalah class abstrak yang menyimpan atribut umum.
- `Patient` dan `Doctor` mewarisi `Person` serta mengimplementasikan ulang
  `get_role()` dan `get_info()`.
- `Appointment` menghubungkan satu pasien dan satu dokter.

------------------------------------------------------------------------

## 2. Class Diagram — Akun dan Hak Akses

```mermaid
classDiagram
    class Account {
        <<abstract>>
        -__id : int
        -__username : str
        -__nama : str
        -__is_active : bool
        +id : int
        +username : str
        +nama : str
        +is_active : bool
        +get_role() str
        +get_role_label() str
        +get_menu_items() list~str~
        +can_manage_patients() bool
        +can_manage_doctors() bool
        +can_manage_accounts() bool
        +can_examine() bool
        +can_book_for_self() bool
    }

    class AdminAccount {
        +get_role() str
        +get_role_label() str
        +get_menu_items() list~str~
        +can_manage_patients() bool
        +can_manage_doctors() bool
        +can_manage_accounts() bool
        +can_examine() bool
    }

    class DoctorAccount {
        -__doctor_id : int
        +doctor_id : int
        +get_role() str
        +get_role_label() str
        +get_menu_items() list~str~
        +can_examine() bool
    }

    class PatientAccount {
        -__patient_id : int
        +patient_id : int
        +get_role() str
        +get_role_label() str
        +get_menu_items() list~str~
        +can_book_for_self() bool
    }

    Account <|-- AdminAccount
    Account <|-- DoctorAccount
    Account <|-- PatientAccount
```

Keterangan:

- `Account` adalah class abstrak untuk akun pengguna.
- `AdminAccount`, `DoctorAccount`, dan `PatientAccount` mewarisi `Account`.
- Setiap subclass mengimplementasikan menu dan hak akses yang berbeda
  (polymorphism).
- `DoctorAccount` terhubung ke satu `Doctor`; `PatientAccount` terhubung ke
  satu `Patient`.

------------------------------------------------------------------------

## 3. Class Diagram — Service dan Repository

```mermaid
classDiagram
    class AuthService {
        -_account_repo : AccountRepository
        -_clinic_repo : ClinicRepository
        +ensure_default_admin() bool
        +login(username, password) Account
        +register_patient(username, password, nama, alamat, no_telepon, tanggal_lahir, jenis_kelamin) PatientAccount
        +create_doctor_account(doctor_id, username, password) int
        +change_password(account_id, old_password, new_password) void
        +reset_password(account_id, new_password) void
        +set_account_active(account_id, is_active) void
        +get_account(account_id) Account
    }

    class AccountRepository {
        -db_path : str
        +create_admin(username, password_hash) int
        +create_patient_account(patient_id, username, password_hash) int
        +create_doctor_account(doctor_id, username, password_hash) int
        +get_by_username(username) Account
        +get_by_id(account_id) Account
        +list_accounts() list~Account~
        +update_password(account_id, password_hash) void
        +set_active(account_id, is_active) void
        +count_admins() int
    }

    class ClinicRepository {
        -db_path : str
        +add_patient(patient) int
        +get_all_patients(keyword) list~Patient~
        +get_patient_by_id(patient_id) Patient
        +get_patient_by_no_rm(no_rm) Patient
        +next_no_rm() str
        +add_doctor(doctor) int
        +get_all_doctors() list~Doctor~
        +create_appointment(appointment) int
        +get_appointments_by_patient(patient_id) list~Appointment~
        +get_appointments_by_doctor(doctor_id) list~Appointment~
        +get_booked_times(doctor_id, tanggal) list~str~
        +update_examination(appointment_id, diagnosis, tindakan) void
        +cancel_appointment(appointment_id) void
        +get_patient_history(patient_id) list~Appointment~
    }

    AuthService --> AccountRepository
    AuthService --> ClinicRepository
    AuthService ..> Account : menggunakan
    AuthService ..> PatientAccount : membuat
    AccountRepository ..> Account : menghasilkan
    ClinicRepository ..> Patient : mengelola
    ClinicRepository ..> Doctor : mengelola
    ClinicRepository ..> Appointment : mengelola
```

------------------------------------------------------------------------

## 4. Class Diagram — Custom Exception

```mermaid
classDiagram
    class ClinicError
    class AppointmentConflictError
    class PatientNotFoundError
    class DoctorNotFoundError
    class DuplicateMedicalRecordError
    class AuthenticationError
    class UsernameAlreadyExistsError
    class AccountNotFoundError
    class InvalidAccountDataError
    class UnauthorizedActionError

    ClinicError <|-- AppointmentConflictError
    ClinicError <|-- PatientNotFoundError
    ClinicError <|-- DoctorNotFoundError
    ClinicError <|-- DuplicateMedicalRecordError
    ClinicError <|-- AuthenticationError
    ClinicError <|-- UsernameAlreadyExistsError
    ClinicError <|-- AccountNotFoundError
    ClinicError <|-- InvalidAccountDataError
    ClinicError <|-- UnauthorizedActionError
```

------------------------------------------------------------------------

## 5. ER Diagram — Struktur Database

```mermaid
erDiagram
    PATIENTS {
        INTEGER id PK
        TEXT no_rm UK
        TEXT nama
        TEXT alamat
        TEXT no_telepon
        TEXT tanggal_lahir
        TEXT jenis_kelamin
    }

    DOCTORS {
        INTEGER id PK
        TEXT nama
        TEXT alamat
        TEXT no_telepon
        TEXT spesialisasi
        TEXT jadwal_praktik
    }

    USERS {
        INTEGER id PK
        TEXT username UK
        TEXT password_hash
        TEXT role
        INTEGER patient_id FK
        INTEGER doctor_id FK
        INTEGER is_active
        TEXT created_at
    }

    APPOINTMENTS {
        INTEGER id PK
        INTEGER patient_id FK
        INTEGER doctor_id FK
        TEXT tanggal
        TEXT waktu
        TEXT keluhan
        TEXT diagnosis
        TEXT tindakan
        TEXT status
    }

    PATIENTS ||--o{ APPOINTMENTS : "memiliki"
    DOCTORS ||--o{ APPOINTMENTS : "menangani"
    PATIENTS ||--o| USERS : "akun pasien"
    DOCTORS ||--o| USERS : "akun dokter"
```

Keterangan:

- Satu pasien dapat memiliki banyak janji; satu dokter dapat menangani
  banyak janji.
- Satu pasien atau dokter memiliki paling banyak satu akun.
- Akun admin tidak terhubung ke `patients` maupun `doctors`.
- `users.username` unik dan `users.password_hash` menyimpan hash password,
  bukan password asli.

------------------------------------------------------------------------

## 6. Activity Diagram — Login, Registrasi, dan Booking Pasien

Diagram ini menggunakan `flowchart` Mermaid sebagai pendekatan activity
diagram.

```mermaid
flowchart TD
    A([Buka aplikasi]) --> B{Sudah login?}
    B -- Belum --> C[Halaman Login / Daftar Pasien]
    C --> D{Pilih aksi}
    D -- Login --> E{Username dan password valid?}
    E -- Tidak --> F[Tampilkan pesan gagal] --> C
    E -- Ya --> G[Dashboard sesuai role]
    D -- Daftar --> H[Isi data pasien dan akun]
    H --> I[Simpan pasien, akun, dan no_rm otomatis]
    I --> C

    G -- Pasien --> J[Tab Buat Janji Temu]
    J --> K[Pilih dokter, tanggal, waktu, dan keluhan]
    K --> L{Jadwal bentrok?}
    L -- Ya --> M[Tampilkan AppointmentConflictError] --> J
    L -- Tidak --> N[Simpan janji berstatus Terjadwal]
    N --> O[Janji Saya / Riwayat Saya]

    G -- Dokter --> P[Janji Saya]
    P --> Q[Isi diagnosis dan tindakan]
    Q --> R[Status janji menjadi Selesai]

    G -- Admin --> S[Kelola pasien, dokter, janji, dan akun]
```

------------------------------------------------------------------------

## 7. Ringkasan Relasi Antar-Class

| Relasi | Jenis | Keterangan |
|---|---|---|
| `Person` → `Patient` | Inheritance | Pasien mewarisi atribut dan method umum. |
| `Person` → `Doctor` | Inheritance | Dokter mewarisi atribut dan method umum. |
| `Appointment` → `Patient` | Association | Janji dimiliki oleh satu pasien. |
| `Appointment` → `Doctor` | Association | Janji ditangani oleh satu dokter. |
| `Account` → `AdminAccount` | Inheritance | Akun admin. |
| `Account` → `DoctorAccount` | Inheritance | Akun dokter. |
| `Account` → `PatientAccount` | Inheritance | Akun pasien. |
| `AuthService` → `AccountRepository` | Dependency | Layanan auth memakai repository akun. |
| `AuthService` → `ClinicRepository` | Dependency | Registrasi pasien memakai repository klinik. |
| `AccountRepository` → `Account` | Dependency | Repository menghasilkan objek akun. |
| `ClinicRepository` → `Patient` | Dependency | Repository mengelola data pasien. |
| `ClinicRepository` → `Doctor` | Dependency | Repository mengelola data dokter. |
| `ClinicRepository` → `Appointment` | Dependency | Repository mengelola janji. |
| `ClinicError` → exception turunan | Inheritance | Seluruh custom exception mewarisi `ClinicError`. |

------------------------------------------------------------------------

