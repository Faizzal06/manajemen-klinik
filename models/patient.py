from .person import Person


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
        self.__no_rm = no_rm
        self.__tanggal_lahir = tanggal_lahir
        self.__jenis_kelamin = jenis_kelamin

    # --- Properties ---
    @property
    def no_rm(self) -> str:
        return self.__no_rm

    @no_rm.setter
    def no_rm(self, value: str) -> None:
        # TODO (Anggota 2): Validasi format nomor rekam medis
        self.__no_rm = value

    @property
    def tanggal_lahir(self) -> str:
        return self.__tanggal_lahir

    @tanggal_lahir.setter
    def tanggal_lahir(self, value: str) -> None:
        self.__tanggal_lahir = value

    @property
    def jenis_kelamin(self) -> str:
        return self.__jenis_kelamin

    @jenis_kelamin.setter
    def jenis_kelamin(self, value: str) -> None:
        # TODO (Anggota 2): Validasi jenis kelamin ('Laki-laki' / 'Perempuan')
        self.__jenis_kelamin = value

    # --- Implementasi Polymorphism ---
    def get_role(self) -> str:
        return "Pasien"

    def get_info(self) -> str:
        # TODO (Anggota 2): Sesuaikan format tampilan ringkasan pasien
        return f"[{self.no_rm}] {self.nama} ({self.jenis_kelamin})"

    def hitung_umur(self) -> int:
        # TODO (Anggota 2): Hitung umur berdasarkan self.tanggal_lahir
        pass