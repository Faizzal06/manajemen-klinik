from models import Account
from exceptions import AccountNotFoundError
from .connection import get_connection


class AccountRepository:
    """Mengelola operasi database untuk tabel users (akun pengguna)."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path

    def _connect(self):
        return get_connection(self.db_path) if self.db_path else get_connection()

    # ==========================================
    # CREATE
    # ==========================================
    def create_admin(self, username: str, password_hash: str) -> int:
        # TODO (Anggota 1): Insert akun admin; raise UsernameAlreadyExistsError jika username duplikat
        pass

    def create_patient_account(
        self, patient_id: int, username: str, password_hash: str
    ) -> int:
        # TODO (Anggota 2): Insert akun pasien yang terhubung ke patient_id
        pass

    def create_doctor_account(
        self, doctor_id: int, username: str, password_hash: str
    ) -> int:
        # TODO (Anggota 3): Insert akun dokter yang terhubung ke doctor_id
        pass

    # ==========================================
    # READ
    # ==========================================
    def get_by_username(self, username: str) -> Account | None:
        # TODO (Anggota 1): Ambil akun berdasarkan username (case-insensitive) beserta nama pasien/dokter
        pass

    def get_by_id(self, account_id: int) -> Account:
        # TODO (Anggota 1): Ambil akun berdasarkan ID; raise AccountNotFoundError jika tidak ada
        pass

    def list_accounts(self) -> list[Account]:
        # TODO (Anggota 1): Ambil semua akun untuk halaman Manajemen Akun
        pass

    def count_admins(self) -> int:
        # TODO (Anggota 1): Hitung akun admin aktif untuk mencegah admin terakhir dinonaktifkan
        pass

    # ==========================================
    # UPDATE / DELETE
    # ==========================================
    def update_password(self, account_id: int, password_hash: str) -> None:
        # TODO (Anggota 1): Simpan password_hash baru
        pass

    def set_active(self, account_id: int, is_active: bool) -> None:
        # TODO (Anggota 1): Aktifkan/nonaktifkan akun
        pass

    def _row_to_account(self, row) -> Account:
        # TODO (Anggota 1): Mapping sqlite3.Row ke AdminAccount / DoctorAccount / PatientAccount
        pass
