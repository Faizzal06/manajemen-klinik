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

    def update_patient(self, patient: Patient) -> None:
        # TODO (Anggota 2): Update data pasien
        pass

    def delete_patient(self, patient_id: int) -> None:
        # TODO (Anggota 2): Hapus data pasien berdasarkan ID
        pass

    # ==========================================
    # CRUD DOKTER (Tanggung Jawab: Anggota 3)
    # ==========================================
    def add_doctor(self, doctor: Doctor) -> int:
        # TODO (Anggota 3): Insert dokter ke tabel doctors
        pass

    def get_all_doctors(self) -> list[Doctor]:
        # TODO (Anggota 3): Ambil seluruh daftar dokter
        pass

    def get_doctor_by_id(self, doctor_id: int) -> Doctor:
        # TODO (Anggota 3): Ambil 1 dokter; raise DoctorNotFoundError jika tidak ada
        pass

    def update_doctor(self, doctor: Doctor) -> None:
        # TODO (Anggota 3): Update data dokter
        pass

    def delete_doctor(self, doctor_id: int) -> None:
        # TODO (Anggota 3): Hapus data dokter berdasarkan ID
        pass

    # ==========================================
    # CRUD JANJI & PEMERIKSAAN (Anggota 4)
    # ==========================================
    def create_appointment(self, appointment: Appointment) -> int:
        # TODO (Anggota 4): Cek bentrok jadwal dokter -> raise AppointmentConflictError jika bentrok, lalu insert
        pass

    def get_all_appointments(self) -> list[Appointment]:
        # TODO (Anggota 4): Ambil semua janji beserta objek Patient & Doctor
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