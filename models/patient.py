import re
from datetime import date

from .person import Person

# Format nomor rekam medis: RM-0001, RM-0002, dst.
_POLA_NO_RM = re.compile(r"RM-(\d{4,})")

# Pemetaan jenis kelamin yang diterima (tanpa membedakan huruf besar/kecil).
_JENIS_KELAMIN = {
    "laki-laki": "Laki-laki",
    "perempuan": "Perempuan",
}


class Patient(Person):
    """Class turunan dari Person untuk mengelola data pasien."""

    def __init__(
        self,
        patient_id: int | None,
        no_rm: str,
        nama: str,
        alamat: str,
        no_telepon: str,
        tanggal_lahir: str,
        jenis_kelamin: str,
    ):
        super().__init__(patient_id, nama, alamat, no_telepon)
        # Lewat setter agar validasi data pasien selalu dijalankan.
        self.no_rm = no_rm
        self.tanggal_lahir = tanggal_lahir
        self.jenis_kelamin = jenis_kelamin

    # --- Properties ---
    @property
    def no_rm(self) -> str:
        return self.__no_rm

    @no_rm.setter
    def no_rm(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Nomor rekam medis harus berformat RM-0001.")

        no_rm = value.strip().upper()
        cocok = _POLA_NO_RM.fullmatch(no_rm)
        if cocok is None or int(cocok.group(1)) < 1:
            raise ValueError("Nomor rekam medis harus berformat RM-0001.")

        self.__no_rm = no_rm

    @property
    def tanggal_lahir(self) -> str:
        return self.__tanggal_lahir

    @tanggal_lahir.setter
    def tanggal_lahir(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Tanggal lahir wajib diisi dengan format YYYY-MM-DD.")

        try:
            tanggal = date.fromisoformat(value.strip())
        except ValueError as exc:
            raise ValueError(
                "Tanggal lahir harus berformat YYYY-MM-DD."
            ) from exc

        if tanggal > date.today():
            raise ValueError("Tanggal lahir tidak boleh di masa depan.")

        self.__tanggal_lahir = tanggal.isoformat()

    @property
    def jenis_kelamin(self) -> str:
        return self.__jenis_kelamin

    @jenis_kelamin.setter
    def jenis_kelamin(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Jenis kelamin harus 'Laki-laki' atau 'Perempuan'.")

        jenis_kelamin = _JENIS_KELAMIN.get(value.strip().lower())
        if jenis_kelamin is None:
            raise ValueError("Jenis kelamin harus 'Laki-laki' atau 'Perempuan'.")

        self.__jenis_kelamin = jenis_kelamin

    # --- Implementasi Polymorphism ---
    def get_role(self) -> str:
        return "Pasien"

    def get_info(self) -> str:
        return (
            f"[{self.no_rm}] {self.nama} "
            f"({self.jenis_kelamin}, {self.hitung_umur()} tahun)"
        )

    def hitung_umur(self) -> int:
        """Menghitung umur pasien berdasarkan tanggal lahir."""
        lahir = date.fromisoformat(self.__tanggal_lahir)
        hari_ini = date.today()
        umur = hari_ini.year - lahir.year
        if (hari_ini.month, hari_ini.day) < (lahir.month, lahir.day):
            umur -= 1
        return max(umur, 0)
