from .patient import Patient
from .doctor import Doctor

class Appointment:
    """Class untuk mengelola janji temu dan catatan pemeriksaan."""

    def __init__(
        self,
        appointment_id: int | None,
        patient: Patient,
        doctor: Doctor,
        tanggal: str,
        waktu: str,
        keluhan: str = "",
        diagnosis: str = "",
        tindakan: str = "",
        status: str = "Terjadwal",
    ):
        self.__id = appointment_id
        self.__patient = patient
        self.__doctor = doctor
        self.__tanggal = tanggal
        self.__waktu = waktu
        self.__keluhan = keluhan
        self.__diagnosis = diagnosis
        self.__tindakan = tindakan
        self.__status = status  # 'Terjadwal', 'Selesai', 'Dibatalkan'

    # --- Properties ---
    @property
    def id(self) -> int | None:
        return self.__id

    @property
    def patient(self) -> Patient:
        return self.__patient

    @property
    def doctor(self) -> Doctor:
        return self.__doctor

    @property
    def tanggal(self) -> str:
        return self.__tanggal

    @property
    def waktu(self) -> str:
        return self.__waktu

    @property
    def keluhan(self) -> str:
        return self.__keluhan

    @keluhan.setter
    def keluhan(self, value: str) -> None:
        self.__keluhan = value

    @property
    def diagnosis(self) -> str:
        return self.__diagnosis

    @diagnosis.setter
    def diagnosis(self, value: str) -> None:
        self.__diagnosis = value

    @property
    def tindakan(self) -> str:
        return self.__tindakan

    @tindakan.setter
    def tindakan(self, value: str) -> None:
        self.__tindakan = value

    @property
    def status(self) -> str:
        return self.__status

    # --- Business Logic Methods ---
    def selesaikan_pemeriksaan(self, diagnosis: str, tindakan: str) -> None:
        # TODO (Anggota 4): Simpan diagnosis, tindakan, dan ubah status menjadi 'Selesai'
        pass

    def batalkan_janji(self) -> None:
        # TODO (Anggota 4): Validasi dan ubah status menjadi 'Dibatalkan'
        pass