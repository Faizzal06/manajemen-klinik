from config import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USERNAME
from database import AccountRepository, ClinicRepository, get_connection
from models import Account, Patient, PatientAccount

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
        """Mendaftarkan pasien baru beserta akun login dalam satu transaksi.

        ``no_rm`` dibuat otomatis. Jika pembuatan akun gagal, data pasien
        ikut dibatalkan sehingga tidak ada pasien tanpa akun.
        """
        username = username.strip()
        validate_username(username)
        validate_password(password)

        nama = (nama or "").strip()
        if not nama:
            raise ValueError("Nama pasien tidak boleh kosong.")

        password_hash = hash_password(password)

        conn = (
            get_connection(self._clinic_repo.db_path)
            if self._clinic_repo.db_path
            else get_connection()
        )
        try:
            patient = Patient(
                patient_id=None,
                no_rm=self._clinic_repo.next_no_rm(conn=conn),
                nama=nama,
                alamat=(alamat or "").strip(),
                no_telepon=(no_telepon or "").strip(),
                tanggal_lahir=tanggal_lahir,
                jenis_kelamin=jenis_kelamin,
            )
            patient_id = self._clinic_repo.add_patient(patient, conn=conn)
            account_id = self._account_repo.create_patient_account(
                patient_id, username, password_hash, conn=conn
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

        return PatientAccount(
            account_id=account_id,
            username=username,
            nama=patient.nama,
            patient_id=patient_id,
        )

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
