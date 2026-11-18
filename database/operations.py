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
    def add_patient(self, patient: Patient) -> int:
        # TODO (Anggota 2): Insert pasien ke tabel patients; raise DuplicateMedicalRecordError jika no_rm duplikat
        pass

    def get_all_patients(self, keyword: str = "") -> list[Patient]:
        # TODO (Anggota 2): Ambil semua pasien atau filter berdasarkan nama / no_rm
        pass

    def get_patient_by_id(self, patient_id: int) -> Patient:
        # TODO (Anggota 2): Ambil 1 pasien; raise PatientNotFoundError jika tidak ada
        pass

    def get_patient_by_no_rm(self, no_rm: str) -> Patient:
        # TODO (Anggota 2): Ambil pasien berdasarkan nomor rekam medis
        pass

    def next_no_rm(self) -> str:
        # TODO (Anggota 2): Buat nomor rekam medis berikutnya dengan format RM-0001
        pass

    def update_patient(self, patient: Patient) -> None:
        # TODO (Anggota 2): Update data pasien
        pass

    def delete_patient(self, patient_id: int) -> None:
        # TODO (Anggota 2): Hapus data pasien berdasarkan ID
        pass

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