import re
import sqlite3

from models import Patient, Doctor, Appointment
from exceptions import (
    AppointmentConflictError,
    PatientNotFoundError,
    DoctorNotFoundError,
    DuplicateMedicalRecordError,
)
from .connection import get_connection


class ClinicRepository:
    """Mengelola seluruh operasi CRUD SQLite untuk Pasien, Dokter, dan Janji."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path

    def _connect(self):
        return get_connection(self.db_path) if self.db_path else get_connection()

    # ==========================================
    # CRUD PASIEN (Tanggung Jawab: Anggota 2)
    # ==========================================
    def _row_to_patient(self, row) -> Patient:
        """Mengubah satu baris tabel patients menjadi objek Patient."""
        return Patient(
            patient_id=row["id"],
            no_rm=row["no_rm"],
            nama=row["nama"],
            alamat=row["alamat"] or "",
            no_telepon=row["no_telepon"] or "",
            tanggal_lahir=row["tanggal_lahir"] or "",
            jenis_kelamin=row["jenis_kelamin"] or "",
        )

    def add_patient(self, patient: Patient, conn=None) -> int:
        """Menyimpan pasien baru dan mengembalikan ID hasil insert.

        Parameter ``conn`` dipakai oleh AuthService agar penyimpanan pasien
        dan akun login dapat berjalan dalam satu transaksi.
        """
        koneksi = conn if conn is not None else self._connect()
        try:
            cursor = koneksi.execute(
                """
                INSERT INTO patients
                    (no_rm, nama, alamat, no_telepon, tanggal_lahir, jenis_kelamin)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    patient.no_rm,
                    patient.nama,
                    patient.alamat,
                    patient.no_telepon,
                    patient.tanggal_lahir,
                    patient.jenis_kelamin,
                ),
            )
            if conn is None:
                koneksi.commit()
            patient.id = int(cursor.lastrowid)
            return patient.id
        except sqlite3.IntegrityError as exc:
            if "patients.no_rm" in str(exc).lower():
                raise DuplicateMedicalRecordError(
                    f"Nomor rekam medis '{patient.no_rm}' sudah terdaftar."
                ) from exc
            raise
        finally:
            if conn is None:
                koneksi.close()

    def get_all_patients(self, keyword: str = "") -> list[Patient]:
        """Mengambil seluruh pasien atau menyaring berdasarkan nama/no_rm."""
        keyword = (keyword or "").strip()
        conn = self._connect()
        try:
            if keyword:
                pola = f"%{keyword}%"
                rows = conn.execute(
                    """
                    SELECT * FROM patients
                    WHERE nama LIKE ? OR no_rm LIKE ?
                    ORDER BY nama COLLATE NOCASE, id
                    """,
                    (pola, pola),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM patients ORDER BY nama COLLATE NOCASE, id"
                ).fetchall()
            return [self._row_to_patient(row) for row in rows]
        finally:
            conn.close()

    def get_patient_by_id(self, patient_id: int) -> Patient:
        """Mengambil satu pasien; raise PatientNotFoundError jika tidak ada."""
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT * FROM patients WHERE id = ?", (patient_id,)
            ).fetchone()
            if row is None:
                raise PatientNotFoundError(
                    f"Pasien dengan ID {patient_id} tidak ditemukan."
                )
            return self._row_to_patient(row)
        finally:
            conn.close()

    def get_patient_by_no_rm(self, no_rm: str) -> Patient:
        """Mengambil pasien berdasarkan nomor rekam medis."""
        no_rm = (no_rm or "").strip().upper()
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT * FROM patients WHERE no_rm = ?", (no_rm,)
            ).fetchone()
            if row is None:
                raise PatientNotFoundError(
                    f"Pasien dengan nomor rekam medis '{no_rm}' tidak ditemukan."
                )
            return self._row_to_patient(row)
        finally:
            conn.close()

    def next_no_rm(self, conn=None) -> str:
        """Membuat nomor rekam medis berikutnya dengan format RM-0001."""
        koneksi = conn if conn is not None else self._connect()
        try:
            rows = koneksi.execute("SELECT no_rm FROM patients").fetchall()
        finally:
            if conn is None:
                koneksi.close()

        nomor_tertinggi = 0
        for row in rows:
            cocok = re.fullmatch(
                r"RM-(\d+)", row["no_rm"] or "", re.IGNORECASE
            )
            if cocok:
                nomor_tertinggi = max(nomor_tertinggi, int(cocok.group(1)))
        return f"RM-{nomor_tertinggi + 1:04d}"

    def update_patient(self, patient: Patient) -> None:
        """Memperbarui data pasien; raise PatientNotFoundError jika tidak ada."""
        if patient.id is None:
            raise PatientNotFoundError("Data pasien belum memiliki ID.")

        conn = self._connect()
        try:
            cursor = conn.execute(
                """
                UPDATE patients
                SET no_rm = ?, nama = ?, alamat = ?, no_telepon = ?,
                    tanggal_lahir = ?, jenis_kelamin = ?
                WHERE id = ?
                """,
                (
                    patient.no_rm,
                    patient.nama,
                    patient.alamat,
                    patient.no_telepon,
                    patient.tanggal_lahir,
                    patient.jenis_kelamin,
                    patient.id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise PatientNotFoundError(
                    f"Pasien dengan ID {patient.id} tidak ditemukan."
                )
        except sqlite3.IntegrityError as exc:
            if "patients.no_rm" in str(exc).lower():
                raise DuplicateMedicalRecordError(
                    f"Nomor rekam medis '{patient.no_rm}' sudah terdaftar."
                ) from exc
            raise
        finally:
            conn.close()

    def delete_patient(self, patient_id: int) -> None:
        """Menghapus pasien; raise PatientNotFoundError jika tidak ada."""
        conn = self._connect()
        try:
            cursor = conn.execute(
                "DELETE FROM patients WHERE id = ?", (patient_id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise PatientNotFoundError(
                    f"Pasien dengan ID {patient_id} tidak ditemukan."
                )
        finally:
            conn.close()

    # ==========================================
    # CRUD DOKTER (Tanggung Jawab: Anggota 3)
    # ==========================================
    def _row_to_doctor(self, row) -> Doctor:
        """Mengubah satu baris tabel doctors menjadi objek Doctor."""
        return Doctor(
            doctor_id=row["id"],
            nama=row["nama"],
            alamat=row["alamat"] or "",
            no_telepon=row["no_telepon"] or "",
            spesialisasi=row["spesialisasi"],
            jadwal_praktik=row["jadwal_praktik"],
        )

    def add_doctor(self, doctor: Doctor) -> int:
        """Menyimpan dokter baru dan mengembalikan ID hasil insert."""
        conn = self._connect()
        try:
            cursor = conn.execute(
                """
                INSERT INTO doctors (nama, alamat, no_telepon, spesialisasi, jadwal_praktik)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    doctor.nama,
                    doctor.alamat,
                    doctor.no_telepon,
                    doctor.spesialisasi,
                    doctor.jadwal_praktik,
                ),
            )
            conn.commit()
            doctor.id = int(cursor.lastrowid)
            return doctor.id
        finally:
            conn.close()

    def get_all_doctors(self) -> list[Doctor]:
        """Mengambil seluruh dokter, diurutkan berdasarkan nama."""
        conn = self._connect()
        try:
            rows = conn.execute(
                "SELECT * FROM doctors ORDER BY nama COLLATE NOCASE, id"
            ).fetchall()
            return [self._row_to_doctor(row) for row in rows]
        finally:
            conn.close()

    def get_doctor_by_id(self, doctor_id: int) -> Doctor:
        """Mengambil satu dokter; raise DoctorNotFoundError jika tidak ada."""
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT * FROM doctors WHERE id = ?", (doctor_id,)
            ).fetchone()
            if row is None:
                raise DoctorNotFoundError(
                    f"Dokter dengan ID {doctor_id} tidak ditemukan."
                )
            return self._row_to_doctor(row)
        finally:
            conn.close()

    def update_doctor(self, doctor: Doctor) -> None:
        """Memperbarui data dokter; raise DoctorNotFoundError jika tidak ada."""
        if doctor.id is None:
            raise DoctorNotFoundError("Data dokter belum memiliki ID.")

        conn = self._connect()
        try:
            cursor = conn.execute(
                """
                UPDATE doctors
                SET nama = ?, alamat = ?, no_telepon = ?, spesialisasi = ?,
                    jadwal_praktik = ?
                WHERE id = ?
                """,
                (
                    doctor.nama,
                    doctor.alamat,
                    doctor.no_telepon,
                    doctor.spesialisasi,
                    doctor.jadwal_praktik,
                    doctor.id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise DoctorNotFoundError(
                    f"Dokter dengan ID {doctor.id} tidak ditemukan."
                )
        finally:
            conn.close()

    def delete_doctor(self, doctor_id: int) -> None:
        """Menghapus dokter; raise DoctorNotFoundError jika tidak ada."""
        conn = self._connect()
        try:
            cursor = conn.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise DoctorNotFoundError(
                    f"Dokter dengan ID {doctor_id} tidak ditemukan."
                )
        finally:
            conn.close()

    # ==========================================
    # CRUD JANJI & PEMERIKSAAN (Anggota 4)
    # ==========================================
    def create_appointment(self, appointment: Appointment) -> int:
        # TODO (Anggota 4): Cek bentrok jadwal dokter -> raise AppointmentConflictError jika bentrok, lalu insert
        pass

    def get_all_appointments(self) -> list[Appointment]:
        # TODO (Anggota 4): Ambil semua janji beserta objek Patient & Doctor
        pass

    def get_appointment_by_id(self, appointment_id: int) -> Appointment:
        # TODO (Anggota 4): Ambil 1 janji; raise error khusus jika tidak ditemukan
        pass

    def get_appointments_by_patient(self, patient_id: int) -> list[Appointment]:
        # TODO (Anggota 4): Ambil janji milik pasien tertentu
        pass

    def get_appointments_by_doctor(self, doctor_id: int) -> list[Appointment]:
        # TODO (Anggota 4): Ambil janji milik dokter tertentu
        pass

    def get_booked_times(self, doctor_id: int, tanggal: str) -> list[str]:
        # TODO (Anggota 4): Ambil daftar waktu yang sudah terisi pada dokter dan tanggal tersebut
        pass

    def update_examination(self, appointment_id: int, diagnosis: str, tindakan: str) -> None:
        # TODO (Anggota 4): Simpan hasil pemeriksaan dan ubah status menjadi 'Selesai'
        pass

    def cancel_appointment(self, appointment_id: int) -> None:
        # TODO (Anggota 4): Ubah status janji menjadi 'Dibatalkan'
        pass

    def get_patient_history(self, patient_id: int) -> list[Appointment]:
        # TODO (Anggota 4): Ambil riwayat kunjungan/pemeriksaan berdasarkan patient_id
        pass

    # ==========================================
    # STATISTIK DASHBOARD (Anggota 1)
    # ==========================================
    def count_patients(self) -> int:
        # TODO (Anggota 1): Hitung total pasien untuk dashboard admin
        pass

    def count_doctors(self) -> int:
        # TODO (Anggota 1): Hitung total dokter untuk dashboard admin
        pass

    def count_active_appointments(self) -> int:
        # TODO (Anggota 1): Hitung janji berstatus 'Terjadwal'
        pass