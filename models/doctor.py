from .person import Person


class Doctor(Person):
    """Class turunan dari Person untuk mengelola data dokter."""

    def __init__(
        self,
        doctor_id: int | None,
        nama: str,
        alamat: str,
        no_telepon: str,
        spesialisasi: str,
        jadwal_praktik: str,
    ):
        super().__init__(doctor_id, nama, alamat, no_telepon)
        self.__spesialisasi = spesialisasi
        self.__jadwal_praktik = jadwal_praktik

    # --- Properties ---
    @property
    def spesialisasi(self) -> str:
        return self.__spesialisasi

    @spesialisasi.setter
    def spesialisasi(self, value: str) -> None:
        self.__spesialisasi = value

    @property
    def jadwal_praktik(self) -> str:
        return self.__jadwal_praktik

    @jadwal_praktik.setter
    def jadwal_praktik(self, value: str) -> None:
        self.__jadwal_praktik = value

    # --- Implementasi Polymorphism ---
    def get_role(self) -> str:
        return "Dokter"

    def get_info(self) -> str:
        # TODO (Anggota 3): Sesuaikan format tampilan ringkasan dokter
        return f"dr. {self.nama} - Spesialis {self.spesialisasi} ({self.jadwal_praktik})"

    def cek_ketersediaan(self, hari: str) -> bool:
        # TODO (Anggota 3): Cek apakah hari masuk dalam jadwal_praktik
        pass