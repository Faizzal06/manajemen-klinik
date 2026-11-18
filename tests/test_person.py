import unittest


class TestPerson(unittest.TestCase):
    """Skeleton pengujian class Person (Anggota 1)."""

    def test_person_adalah_abstract_class(self):
        # TODO: Pastikan Person tidak dapat diinstansiasi langsung.
        pass

    def test_validasi_nama_tidak_boleh_kosong(self):
        # TODO: Uji setter nama dengan string kosong.
        pass

    def test_validasi_format_nomor_telepon(self):
        # TODO: Uji setter no_telepon dengan format yang tidak valid.
        pass


if __name__ == "__main__":
    unittest.main()
