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

## 2. Tujuan

1.  Mempermudah pengelolaan data pasien dan dokter.
2.  Membantu pencatatan serta pengelolaan janji pemeriksaan.
3.  Menyimpan informasi pemeriksaan dan riwayat kunjungan pasien.
4.  Menerapkan konsep Encapsulation, Inheritance, dan Polymorphism.
5.  Menerapkan pengujian unit menggunakan `unittest`.

## 3. Ruang Lingkup Fitur

  -----------------------------------------------------------------------
  Fitur                               Deskripsi
  ----------------------------------- -----------------------------------
  Dashboard                           Menampilkan ringkasan jumlah
                                      pasien, dokter, dan janji
                                      pemeriksaan.

  Manajemen Pasien                    Menambah, melihat, mengubah,
                                      menghapus, dan mencari data pasien.

  Manajemen Dokter                    Mengelola data dokter,
                                      spesialisasi, dan jadwal praktik.

  Janji Pemeriksaan                   Membuat, melihat, dan membatalkan
                                      janji pemeriksaan.

  Pemeriksaan                         Mencatat keluhan, diagnosis,
                                      tindakan, dan status pemeriksaan.

  Riwayat Kunjungan                   Menampilkan riwayat pemeriksaan
                                      berdasarkan pasien.
  -----------------------------------------------------------------------

## 4. Teknologi

-   **Python:** bahasa pemrograman utama.
-   **Streamlit:** antarmuka web responsif.
-   **SQLite:** basis data relasional lokal.
-   **`unittest`:** pengujian unit bawaan Python.

**Catatan akses mobile:** Streamlit bukan aplikasi Android native.
Aplikasi dibuka melalui browser. Untuk pengujian melalui ponsel dalam
jaringan Wi-Fi yang sama, server Streamlit perlu dijalankan agar dapat
diakses dari jaringan lokal. Akses melalui internet memerlukan
deployment/hosting.

## 5. Rancangan Class Utama

Pembagian berikut merupakan rancangan awal untuk kelompok beranggotakan
empat orang. Setiap anggota bertanggung jawab atas satu class utama,
termasuk implementasi, pengujian, dan dokumentasinya.

  -----------------------------------------------------------------------
  Anggota                 Class                   Tanggung jawab
  ----------------------- ----------------------- -----------------------
  1                       `Person`                Class induk yang
                                                  menyimpan informasi
                                                  umum seseorang.

  2                       `Patient`               Mengelola data dan
                                                  informasi pasien.

  3                       `Doctor`                Mengelola data dokter,
                                                  spesialisasi, dan
                                                  jadwal praktik.

  4                       `Appointment`           Mengelola janji dan
                                                  catatan pemeriksaan.
  -----------------------------------------------------------------------

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

## 6. Penerapan Konsep PBO

1.  **Encapsulation:** atribut penting dibuat terlindungi (misalnya
    menggunakan atribut private) dan diakses melalui method atau
    `@property`.
2.  **Inheritance:** `Patient` dan `Doctor` mewarisi atribut serta
    perilaku umum dari `Person`.
3.  **Polymorphism:** `Patient` dan `Doctor` dapat mengimplementasikan
    ulang method seperti `get_info()` atau `get_role()` sesuai
    karakteristik masing-masing.
4.  **Custom Exception:** membuat exception khusus, misalnya
    `AppointmentConflictError`, `PatientNotFoundError`, atau
    `DoctorNotFoundError`, untuk menangani kondisi kesalahan aplikasi.

## 7. Rancangan Basis Data

Tabel utama yang direncanakan:

  -----------------------------------------------------------------------
  Tabel                               Kolom penting
  ----------------------------------- -----------------------------------
  `patients`                          `id`, `no_rm`, `nama`, `alamat`,
                                      `no_telepon`, `tanggal_lahir`,
                                      `jenis_kelamin`

  `doctors`                           `id`, `nama`, `alamat`,
                                      `no_telepon`, `spesialisasi`,
                                      `jadwal_praktik`

  `appointments`                      `id`, `patient_id`, `doctor_id`,
                                      `tanggal`, `waktu`, `keluhan`,
                                      `diagnosis`, `tindakan`, `status`
  -----------------------------------------------------------------------

Relasi: - Satu pasien dapat memiliki banyak janji pemeriksaan. - Satu
dokter dapat menangani banyak janji pemeriksaan. -
`appointments.patient_id` menjadi foreign key ke `patients.id`. -
`appointments.doctor_id` menjadi foreign key ke `doctors.id`.

Nomor rekam medis (`no_rm`) direncanakan unik. Validasi juga diperlukan
untuk memastikan pasien dan dokter tersedia serta mencegah bentrok
jadwal dokter.

## 8. Rancangan Antarmuka

Navigasi utama aplikasi:

1.  Dashboard
2.  Manajemen Pasien
3.  Manajemen Dokter
4.  Janji Pemeriksaan
5.  Pemeriksaan
6.  Riwayat Kunjungan

Antarmuka dirancang sederhana dan responsif. Formulir diupayakan tetap
nyaman digunakan pada layar ponsel, sementara tabel data perlu disajikan
agar tetap mudah dibaca pada layar kecil.

## 9. Struktur Folder Awal

``` text
ClinicManagementSystem/
├── main.py
├── models/
│   ├── __init__.py
│   ├── person.py
│   ├── patient.py
│   ├── doctor.py
│   └── appointment.py
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── schema.py
│   └── operations.py
├── exceptions/
│   ├── __init__.py
│   └── clinic_exceptions.py
├── ui/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── patients.py
│   ├── doctors.py
│   ├── appointments.py
│   └── history.py
├── tests/
│   ├── test_person.py
│   ├── test_patient.py
│   ├── test_doctor.py
│   └── test_appointment.py
├── data/
│   └── clinic.db
├── docs/
├── requirements.txt
└── README.md
```

## 10. Pembagian Pekerjaan Awal

Pembagian class utama mengikuti tabel pada bagian 5. Untuk pekerjaan
antarmuka dan integrasi, pembagian dapat dilakukan sebagai berikut:

-   **Anggota 1:** koordinasi integrasi, class `Person`, dan kerangka
    aplikasi.
-   **Anggota 2:** class `Patient` dan halaman Manajemen Pasien.
-   **Anggota 3:** class `Doctor` dan halaman Manajemen Dokter.
-   **Anggota 4:** class `Appointment` dan halaman Janji/Pemeriksaan.

Seluruh anggota tetap perlu berkoordinasi untuk integrasi database,
pengujian aplikasi, dokumentasi, dan penyelesaian laporan.

## 11. Rencana Pengerjaan

  -----------------------------------------------------------------------
  Tahap                               Target
  ----------------------------------- -----------------------------------
  Pertemuan 11                        Menentukan tema, anggota, pembagian
                                      class, rancangan UML, dan rancangan
                                      awal.

  Pertemuan 12                        Membuat skeleton code class,
                                      atribut, method, struktur proyek,
                                      dan skema database.

  Pertemuan 13                        Mengimplementasikan class, Custom
                                      Exception, CRUD, dan unit test
                                      awal.

  Pertemuan 14                        Mengintegrasikan antarmuka, class,
                                      database, serta menyelesaikan
                                      pengujian dan dokumentasi.

  Pertemuan 15                        Menyerahkan source code ZIP,
                                      laporan PDF beserta logbook, dan
                                      video presentasi.
  -----------------------------------------------------------------------

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

Untuk mengakses aplikasi dari perangkat lain dalam jaringan lokal yang
sama:

``` bash
streamlit run main.py --server.address 0.0.0.0
```

