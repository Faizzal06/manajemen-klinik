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


class AuthenticationError(ClinicError):
    """Dilempar jika login gagal atau kredensial tidak valid."""
    pass


class UsernameAlreadyExistsError(ClinicError):
    """Dilempar jika username akun sudah digunakan."""
    pass


class AccountNotFoundError(ClinicError):
    """Dilempar jika akun pengguna tidak ditemukan."""
    pass


class InvalidAccountDataError(ClinicError):
    """Dilempar jika data akun (username/password) tidak valid."""
    pass


class UnauthorizedActionError(ClinicError):
    """Dilempar jika pengguna mencoba melakukan aksi di luar hak aksesnya."""
    pass