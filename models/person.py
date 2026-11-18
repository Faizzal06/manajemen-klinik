from abc import ABC, abstractmethod


class Person(ABC):
    """Class induk (abstract) yang menyimpan informasi umum seseorang."""

    def __init__(self, person_id: int | None, nama: str, alamat: str, no_telepon: str):
        # Encapsulation: atribut private
        self.__id = person_id
        self.__nama = nama
        self.__alamat = alamat
        self.__no_telepon = no_telepon

    # --- Properties (Getter & Setter) ---
    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, value: int | None) -> None:
        self.__id = value

    @property
    def nama(self) -> str:
        return self.__nama

    @nama.setter
    def nama(self, value: str) -> None:
        # TODO (Anggota 1): Tambahkan validasi nama tidak boleh kosong
        self.__nama = value

    @property
    def alamat(self) -> str:
        return self.__alamat

    @alamat.setter
    def alamat(self, value: str) -> None:
        self.__alamat = value

    @property
    def no_telepon(self) -> str:
        return self.__no_telepon

    @no_telepon.setter
    def no_telepon(self, value: str) -> None:
        # TODO (Anggota 1): Tambahkan validasi format nomor telepon
        self.__no_telepon = value

    # --- Polymorphism Methods ---
    @abstractmethod
    def get_role(self) -> str:
        """Mengembalikan peran objek (misal: 'Pasien' atau 'Dokter')."""
        pass

    @abstractmethod
    def get_info(self) -> str:
        """Mengembalikan ringkasan informasi spesifik objek."""
        pass