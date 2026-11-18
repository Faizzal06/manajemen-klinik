class ClinicError(Exception):
    """Base exception untuk seluruh error di Sistem Manajemen Klinik."""
    pass


class AppointmentConflictError(ClinicError):
    """Dilempar jika jadwal dokter bentrok pada tanggal dan waktu yang sama."""
    pass


class PatientNotFoundError(ClinicError):
    """Dilempar jika data pasien tidak ditemukan."""
    pass


class DoctorNotFoundError(ClinicError):
    """Dilempar jika data dokter tidak ditemukan."""
    pass


class DuplicateMedicalRecordError(ClinicError):
    """Dilempar jika nomor rekam medis (no_rm) sudah terdaftar."""
    pass