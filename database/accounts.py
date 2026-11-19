import sqlite3

from models import Account
from exceptions import (
    AccountNotFoundError,
    DoctorNotFoundError,
    InvalidAccountDataError,
    PatientNotFoundError,
    UsernameAlreadyExistsError,
)
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
        self,
        patient_id: int,
        username: str,
        password_hash: str,
        conn=None,
    ) -> int:
        """Membuat akun login pasien yang terhubung ke patient_id.

        Parameter ``conn`` dipakai oleh AuthService agar data pasien dan akun
        dapat disimpan dalam satu transaksi.
        """
        koneksi = conn if conn is not None else self._connect()
        try:
            cursor = koneksi.execute(
                """
                INSERT INTO users (username, password_hash, role, patient_id)
                VALUES (?, ?, 'pasien', ?)
                """,
                (username, password_hash, patient_id),
            )
            if conn is None:
                koneksi.commit()
            return int(cursor.lastrowid)
        except sqlite3.IntegrityError as exc:
            pesan = str(exc).lower()
            if "users.username" in pesan:
                raise UsernameAlreadyExistsError(
                    f"Username '{username}' sudah digunakan."
                ) from exc
            if "users.patient_id" in pesan:
                raise InvalidAccountDataError(
                    "Pasien ini sudah memiliki akun login."
                ) from exc
            if "foreign key" in pesan:
                raise PatientNotFoundError(
                    f"Pasien dengan ID {patient_id} tidak ditemukan."
                ) from exc
            raise
        finally:
            if conn is None:
                koneksi.close()

    def create_doctor_account(
        self, doctor_id: int, username: str, password_hash: str
    ) -> int:
        """Membuat akun login untuk dokter dan mengembalikan ID akun."""
        conn = self._connect()
        try:
            cursor = conn.execute(
                """
                INSERT INTO users (username, password_hash, role, doctor_id)
                VALUES (?, ?, 'dokter', ?)
                """,
                (username, password_hash, doctor_id),
            )
            conn.commit()
            return int(cursor.lastrowid)
        except sqlite3.IntegrityError as exc:
            pesan = str(exc).lower()
            if "users.username" in pesan:
                raise UsernameAlreadyExistsError(
                    f"Username '{username}' sudah digunakan."
                ) from exc
            if "users.doctor_id" in pesan:
                raise InvalidAccountDataError(
                    "Dokter ini sudah memiliki akun login."
                ) from exc
            if "foreign key" in pesan:
                raise DoctorNotFoundError(
                    f"Dokter dengan ID {doctor_id} tidak ditemukan."
                ) from exc
            raise
        finally:
            conn.close()

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
