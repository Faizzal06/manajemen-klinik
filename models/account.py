from abc import ABC, abstractmethod


class Account(ABC):
    """Class abstrak untuk akun pengguna sistem (admin, dokter, pasien)."""

    def __init__(
        self,
        account_id: int | None,
        username: str,
        nama: str,
        is_active: bool = True,
    ):
        # Encapsulation: atribut private
        self.__id = account_id
        self.__username = username
        self.__nama = nama
        self.__is_active = is_active

    # --- Properties ---
    @property
    def id(self) -> int | None:
        return self.__id

    @property
    def username(self) -> str:
        return self.__username

    @property
    def nama(self) -> str:
        return self.__nama

    @property
    def is_active(self) -> bool:
        return self.__is_active

    # --- Polymorphism Methods ---
    @abstractmethod
    def get_role(self) -> str:
        """Mengembalikan kode role: 'admin', 'dokter', atau 'pasien'."""
        pass

    @abstractmethod
    def get_role_label(self) -> str:
        """Mengembalikan label role untuk ditampilkan di antarmuka."""
        pass

    @abstractmethod
    def get_menu_items(self) -> list[str]:
        """Mengembalikan daftar menu sidebar sesuai hak akses role."""
        pass

    # --- Hak Akses (dapat di-override oleh subclass) ---
    def can_manage_patients(self) -> bool:
        return False

    def can_manage_doctors(self) -> bool:
        return False

    def can_manage_accounts(self) -> bool:
        return False

    def can_examine(self) -> bool:
        return False

    def can_book_for_self(self) -> bool:
        return False


class AdminAccount(Account):
    """Akun admin/petugas dengan akses pengelolaan klinik."""

    def get_role(self) -> str:
        return "admin"

    def get_role_label(self) -> str:
        return "Admin / Petugas"

    def get_menu_items(self) -> list[str]:
        return [
            "Dashboard",
            "Manajemen Pasien",
            "Manajemen Dokter",
            "Janji & Pemeriksaan",
            "Riwayat Kunjungan",
            "Manajemen Akun",
            "Akun Saya",
        ]

    def can_manage_patients(self) -> bool:
        return True

    def can_manage_doctors(self) -> bool:
        return True

    def can_manage_accounts(self) -> bool:
        return True

    def can_examine(self) -> bool:
        return True


class DoctorAccount(Account):
    """Akun dokter yang terhubung ke satu data dokter."""

    def __init__(
        self,
        account_id: int | None,
        username: str,
        nama: str,
        doctor_id: int,
        is_active: bool = True,
    ):
        super().__init__(account_id, username, nama, is_active)
        self.__doctor_id = doctor_id

    @property
    def doctor_id(self) -> int:
        return self.__doctor_id

    def get_role(self) -> str:
        return "dokter"

    def get_role_label(self) -> str:
        return "Dokter"

    def get_menu_items(self) -> list[str]:
        return [
            "Dashboard",
            "Janji Saya",
            "Pemeriksaan",
            "Riwayat Pasien",
            "Akun Saya",
        ]

    def can_examine(self) -> bool:
        return True


class PatientAccount(Account):
    """Akun pasien yang terhubung ke satu data pasien."""

    def __init__(
        self,
        account_id: int | None,
        username: str,
        nama: str,
        patient_id: int,
        is_active: bool = True,
    ):
        super().__init__(account_id, username, nama, is_active)
        self.__patient_id = patient_id

    @property
    def patient_id(self) -> int:
        return self.__patient_id

    def get_role(self) -> str:
        return "pasien"

    def get_role_label(self) -> str:
        return "Pasien"

    def get_menu_items(self) -> list[str]:
        return [
            "Dashboard",
            "Akun Saya",
        ]

    def can_book_for_self(self) -> bool:
        return True
