import unittest


class TestAppointment(unittest.TestCase):
    """Skeleton pengujian class Appointment (Anggota 4)."""

    def test_selesaikan_pemeriksaan(self):
        # TODO: Uji pengisian diagnosis/tindakan dan perubahan status menjadi 'Selesai'.
        pass

    def test_batalkan_janji(self):
        # TODO: Uji pembatalan janji dan validasi status.
        pass

    def test_bentrok_jadwal(self):
        # TODO: Uji AppointmentConflictError pada dokter, tanggal, dan waktu yang sama.
        pass


if __name__ == "__main__":
    unittest.main()
