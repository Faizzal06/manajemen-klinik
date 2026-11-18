import unittest


class TestPatient(unittest.TestCase):
    """Skeleton pengujian class Patient (Anggota 2)."""

    def test_patient_mewarisi_person(self):
        # TODO: Pastikan Patient adalah instance dari Person.
        pass

    def test_validasi_no_rm(self):
        # TODO: Uji format nomor rekam medis.
        pass

    def test_validasi_jenis_kelamin(self):
        # TODO: Uji nilai jenis kelamin selain 'Laki-laki' / 'Perempuan'.
        pass

    def test_hitung_umur(self):
        # TODO: Uji perhitungan umur dari tanggal lahir.
        pass


if __name__ == "__main__":
    unittest.main()
