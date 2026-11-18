import re

from .person import Person

# Nama hari yang dikenali pada pengecekan jadwal praktik.
# Nilai tuple berisi variasi penulisan yang dianggap sama.
_HARI_PRAKTIK = {
    "senin": ("senin",),
    "selasa": ("selasa",),
    "rabu": ("rabu",),
    "kamis": ("kamis",),
    "jumat": ("jumat", "jum'at", "jumaat"),
    "sabtu": ("sabtu",),
    "minggu": ("minggu", "ahad"),
}

# Variasi penulisan yang dipetakan ke nama hari utama.
_ALIAS_HARI = {
    "jum'at": "jumat",
    "jumaat": "jumat",
    "ahad": "minggu",
}


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
        # Lewat setter agar validasi data dokter selalu dijalankan.
        self.spesialisasi = spesialisasi
        self.jadwal_praktik = jadwal_praktik

    # --- Properties ---
    @property
    def spesialisasi(self) -> str:
        return self.__spesialisasi

    @spesialisasi.setter
    def spesialisasi(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Spesialisasi dokter tidak boleh kosong.")
        self.__spesialisasi = value.strip()

    @property
    def jadwal_praktik(self) -> str:
        return self.__jadwal_praktik

    @jadwal_praktik.setter
    def jadwal_praktik(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Jadwal praktik dokter tidak boleh kosong.")
        self.__jadwal_praktik = value.strip()

    # --- Implementasi Polymorphism ---
    def get_role(self) -> str:
        return "Dokter"

    def get_info(self) -> str:
        return (
            f"dr. {self.nama} - Spesialis {self.spesialisasi} "
            f"({self.jadwal_praktik})"
        )

    def cek_ketersediaan(self, hari: str) -> bool:
        """Cek apakah nama hari termasuk dalam teks jadwal praktik.

        Pencocokan dilakukan tanpa membedakan huruf besar/kecil dan hanya
        menerima nama hari sebagai kata utuh, sehingga "senin" tidak ikut
        cocok dengan kata lain yang mengandung "senin". Hari yang tidak
        dikenali atau jadwal kosong dianggap tidak tersedia (False).
        """
        if not isinstance(hari, str):
            return False

        nama_hari = hari.strip().lower()
        nama_hari = _ALIAS_HARI.get(nama_hari, nama_hari)
        variasi_hari = _HARI_PRAKTIK.get(nama_hari)
        if not variasi_hari:
            return False

        jadwal = self.jadwal_praktik.lower()
        for variasi in variasi_hari:
            pola = rf"\b{re.escape(variasi)}\b"
            if re.search(pola, jadwal):
                return True
        return False
