import os
import tempfile
import unittest

from database import ClinicRepository, init_db
from exceptions import DoctorNotFoundError
from models import Doctor


class TestClinicRepository(unittest.TestCase):
    """Skeleton pengujian CRUD repository (seluruh anggota)."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = os.path.join(self.temp_dir.name, "test_clinic.db")
        init_db(self.db_path)
        self.repo = ClinicRepository(self.db_path)

    def test_crud_pasien(self):
        # TODO: Uji tambah, cari, ubah, dan hapus pasien.
        pass

    def test_crud_dokter(self):
        dokter = Doctor(
            doctor_id=None,
            nama="Andi Pratama",
            alamat="Jl. Merdeka No. 1",
            no_telepon="081234567890",
            spesialisasi="Umum",
            jadwal_praktik="Senin - Jumat, 08.00 - 12.00",
        )

        doctor_id = self.repo.add_doctor(dokter)

        tersimpan = self.repo.get_doctor_by_id(doctor_id)
        self.assertEqual(tersimpan.nama, "Andi Pratama")
        self.assertEqual(tersimpan.spesialisasi, "Umum")
        self.assertEqual(len(self.repo.get_all_doctors()), 1)

        tersimpan.spesialisasi = "Anak"
        self.repo.update_doctor(tersimpan)
        self.assertEqual(self.repo.get_doctor_by_id(doctor_id).spesialisasi, "Anak")

        self.repo.delete_doctor(doctor_id)
        with self.assertRaises(DoctorNotFoundError):
            self.repo.get_doctor_by_id(doctor_id)

    def test_no_rm_duplikat_ditolak(self):
        # TODO: Uji DuplicateMedicalRecordError.
        pass

    def test_slot_waktu_terisi(self):
        # TODO: Uji get_booked_times() pada dokter dan tanggal tertentu.
        pass


if __name__ == "__main__":
    unittest.main()
