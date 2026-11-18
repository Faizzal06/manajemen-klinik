import unittest


class TestClinicRepository(unittest.TestCase):
    """Skeleton pengujian CRUD repository (seluruh anggota)."""

    def test_crud_pasien(self):
        # TODO: Uji tambah, cari, ubah, dan hapus pasien.
        pass

    def test_crud_dokter(self):
        # TODO: Uji tambah, ubah, dan hapus dokter.
        pass

    def test_no_rm_duplikat_ditolak(self):
        # TODO: Uji DuplicateMedicalRecordError.
        pass

    def test_slot_waktu_terisi(self):
        # TODO: Uji get_booked_times() pada dokter dan tanggal tertentu.
        pass


if __name__ == "__main__":
    unittest.main()
