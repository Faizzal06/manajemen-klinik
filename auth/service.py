from config import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USERNAME
from database import AccountRepository, ClinicRepository
from models import Account, PatientAccount

from .security import hash_password, validate_password, validate_username


class AuthService:
    """Layanan autentikasi, registrasi, dan pengelolaan akun pengguna."""

    def __init__(
        self,
        account_repo: AccountRepository,
        clinic_repo: ClinicRepository,
    ):
        self._account_repo = account_repo
        self._clinic_repo = clinic_repo

    def ensure_default_admin(self) -> bool:
        # TODO (Anggota 1): Buat admin default hanya jika belum ada akun admin.
        # Gunakan DEFAULT_ADMIN_USERNAME dan DEFAULT_ADMIN_PASSWORD dari config.py.
        pass

    def login(self, username: str, password: str) -> Account:
        # TODO (Anggota 1): Cari akun, verifikasi password, cek is_active.
        # Raise AuthenticationError dengan pesan generik jika gagal.
        pass

    def register_patient(
        self,
        username: str,
        password: str,
        nama: str,
        alamat: str,
        no_telepon: str,
        tanggal_lahir: str,
        jenis_kelamin: str,
    ) -> PatientAccount:
        # TODO (Anggota 2): Validasi input, buat no_rm otomatis, simpan pasien + akun
        # dalam satu transaksi, lalu kembalikan PatientAccount.
        pass

    def create_doctor_account(
        self, doctor_id: int, username: str, password: str
    ) -> int:
        """Membuat akun login dokter setelah validasi data akun.

        Raise DoctorNotFoundError jika data dokter tidak ada, serta
        UsernameAlreadyExistsError / InvalidAccountDataError jika data akun
        tidak valid atau sudah dipakai.
        """
        self._clinic_repo.get_doctor_by_id(doctor_id)

        username = username.strip()
        validate_username(username)
        validate_password(password)

        password_hash = hash_password(password)
        return self._account_repo.create_doctor_account(
            doctor_id, username, password_hash
        )

    def change_password(
        self, account_id: int, old_password: str, new_password: str
    ) -> None:
        # TODO (Anggota 1): Verifikasi password lama sebelum menyimpan password baru.
        pass

    def reset_password(self, account_id: int, new_password: str) -> None:
        # TODO (Anggota 1): Reset password oleh admin.
        pass

    def set_account_active(self, account_id: int, is_active: bool) -> None:
        # TODO (Anggota 1): Aktifkan/nonaktifkan akun; cegah menonaktifkan admin terakhir.
        pass

    def get_account(self, account_id: int) -> Account:
        # TODO (Anggota 1): Delegasikan ke AccountRepository.get_by_id.
        pass
