import os
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

try:
    import streamlit  # noqa: F401
except ModuleNotFoundError:
    # auth/__init__.py mengimpor session.py yang membutuhkan Streamlit.
    # Stub minimal ini menjaga unit test tetap dapat berjalan tanpa dependency UI.
    sys.modules["streamlit"] = types.ModuleType("streamlit")

from auth.service import AuthService
from database import AccountRepository, ClinicRepository, get_connection, init_db
from exceptions import (
    DoctorNotFoundError,
    InvalidAccountDataError,
    UsernameAlreadyExistsError,
)
from models import Doctor, Person


def buat_dokter(**perubahan) -> Doctor:
    """Membuat objek Doctor dengan data valid sebagai dasar pengujian."""
    data = {
        "doctor_id": None,
        "nama": "Andi Pratama",
        "alamat": "Jl. Merdeka No. 1",
        "no_telepon": "081234567890",
        "spesialisasi": "Umum",
        "jadwal_praktik": "Senin - Jumat, 08.00 - 12.00",
    }
    data.update(perubahan)
    return Doctor(**data)


class TestDoctor(unittest.TestCase):
    """Pengujian class Doctor (Anggota 3)."""

    def test_doctor_mewarisi_person(self):
        dokter = buat_dokter()

        self.assertIsInstance(dokter, Person)
        self.assertIsInstance(dokter, Doctor)

    def test_get_role_dokter(self):
        self.assertEqual(buat_dokter().get_role(), "Dokter")

    def test_get_info_dokter(self):
        dokter = buat_dokter()

        self.assertEqual(
            dokter.get_info(),
            "dr. Andi Pratama - Spesialis Umum "
            "(Senin - Jumat, 08.00 - 12.00)",
        )

    def test_spesialisasi_dan_jadwal_dirapikan(self):
        dokter = buat_dokter(
            spesialisasi="  Anak  ",
            jadwal_praktik="  Selasa, 09.00 - 13.00  ",
        )

        self.assertEqual(dokter.spesialisasi, "Anak")
        self.assertEqual(dokter.jadwal_praktik, "Selasa, 09.00 - 13.00")

    def test_spesialisasi_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            buat_dokter(spesialisasi="   ")

    def test_jadwal_praktik_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            buat_dokter(jadwal_praktik="")

    def test_setter_spesialisasi_kosong_ditolak(self):
        dokter = buat_dokter()

        with self.assertRaises(ValueError):
            dokter.spesialisasi = "  "

    def test_setter_jadwal_praktik_kosong_ditolak(self):
        dokter = buat_dokter()

        with self.assertRaises(ValueError):
            dokter.jadwal_praktik = ""

    def test_cek_ketersediaan_hari_dikenali(self):
        dokter = buat_dokter()

        self.assertTrue(dokter.cek_ketersediaan("Senin"))
        self.assertTrue(dokter.cek_ketersediaan("senin"))
        self.assertTrue(dokter.cek_ketersediaan("Jumat"))
        self.assertTrue(dokter.cek_ketersediaan("jum'at"))

    def test_cek_ketersediaan_tanpa_beda_huruf_besar_kecil(self):
        dokter = buat_dokter(
            jadwal_praktik="Senin dan Rabu, 08.00 - 12.00"
        )

        self.assertTrue(dokter.cek_ketersediaan("  RABU  "))

    def test_cek_ketersediaan_hari_tidak_ada(self):
        dokter = buat_dokter()

        self.assertFalse(dokter.cek_ketersediaan("Sabtu"))
        self.assertFalse(dokter.cek_ketersediaan("Minggu"))

    def test_cek_ketersediaan_alias_minggu_ahad(self):
        dokter = buat_dokter(jadwal_praktik="Minggu, 09.00 - 12.00")

        self.assertTrue(dokter.cek_ketersediaan("Ahad"))
        self.assertTrue(dokter.cek_ketersediaan("minggu"))

    def test_cek_ketersediaan_hari_tidak_dikenal(self):
        dokter = buat_dokter()

        self.assertFalse(dokter.cek_ketersediaan("Hari Libur"))
        self.assertFalse(dokter.cek_ketersediaan(""))
        self.assertFalse(dokter.cek_ketersediaan(None))

    def test_cek_ketersediaan_berbagai_hari_dalam_teks(self):
        dokter = buat_dokter(
            jadwal_praktik="Senin, 08.00 - 12.00; Rabu, 13.00 - 17.00"
        )

        self.assertTrue(dokter.cek_ketersediaan("Senin"))
        self.assertTrue(dokter.cek_ketersediaan("Rabu"))
        self.assertFalse(dokter.cek_ketersediaan("Kamis"))


class TestDoctorRepository(unittest.TestCase):
    """Pengujian CRUD dokter pada ClinicRepository (Anggota 3)."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = os.path.join(self.temp_dir.name, "test_clinic.db")
        init_db(self.db_path)
        self.repo = ClinicRepository(self.db_path)

    def test_tambah_dan_ambil_dokter(self):
        dokter = buat_dokter()

        doctor_id = self.repo.add_doctor(dokter)

        self.assertIsInstance(doctor_id, int)
        self.assertGreater(doctor_id, 0)
        self.assertEqual(dokter.id, doctor_id)

        tersimpan = self.repo.get_doctor_by_id(doctor_id)
        self.assertEqual(tersimpan.nama, "Andi Pratama")
        self.assertEqual(tersimpan.spesialisasi, "Umum")
        self.assertEqual(tersimpan.jadwal_praktik, "Senin - Jumat, 08.00 - 12.00")
        self.assertEqual(tersimpan.alamat, "Jl. Merdeka No. 1")
        self.assertEqual(tersimpan.no_telepon, "081234567890")

    def test_get_all_doctors_urut_nama(self):
        self.repo.add_doctor(buat_dokter(nama="Budi Santoso"))
        self.repo.add_doctor(buat_dokter(nama="Andi Pratama"))

        daftar = self.repo.get_all_doctors()

        self.assertEqual([dokter.nama for dokter in daftar], ["Andi Pratama", "Budi Santoso"])

    def test_update_dokter(self):
        doctor_id = self.repo.add_doctor(buat_dokter())
        dokter = self.repo.get_doctor_by_id(doctor_id)
        dokter.spesialisasi = "Anak"
        dokter.jadwal_praktik = "Selasa, 09.00 - 13.00"
        dokter.no_telepon = "089999999999"

        self.repo.update_doctor(dokter)

        diperbarui = self.repo.get_doctor_by_id(doctor_id)
        self.assertEqual(diperbarui.spesialisasi, "Anak")
        self.assertEqual(diperbarui.jadwal_praktik, "Selasa, 09.00 - 13.00")
        self.assertEqual(diperbarui.no_telepon, "089999999999")

    def test_ambil_dokter_tidak_ditemukan(self):
        with self.assertRaises(DoctorNotFoundError):
            self.repo.get_doctor_by_id(9999)

    def test_update_dokter_tidak_ditemukan(self):
        dokter = buat_dokter(doctor_id=9999)

        with self.assertRaises(DoctorNotFoundError):
            self.repo.update_doctor(dokter)

    def test_delete_dokter(self):
        doctor_id = self.repo.add_doctor(buat_dokter())

        self.repo.delete_doctor(doctor_id)

        with self.assertRaises(DoctorNotFoundError):
            self.repo.get_doctor_by_id(doctor_id)
        with self.assertRaises(DoctorNotFoundError):
            self.repo.delete_doctor(doctor_id)


class TestDoctorAccount(unittest.TestCase):
    """Pengujian pembuatan akun login dokter (Anggota 3)."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = os.path.join(self.temp_dir.name, "test_clinic.db")
        init_db(self.db_path)
        self.repo = ClinicRepository(self.db_path)
        self.account_repo = AccountRepository(self.db_path)
        self.auth_service = AuthService(self.account_repo, self.repo)
        self.doctor_id = self.repo.add_doctor(buat_dokter())

    def _hitung_akun(self) -> int:
        conn = get_connection(self.db_path)
        try:
            return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        finally:
            conn.close()

    def test_create_doctor_account_di_repository(self):
        account_id = self.account_repo.create_doctor_account(
            self.doctor_id, "dokter.andi", "hash-palsu"
        )

        self.assertGreater(account_id, 0)
        conn = get_connection(self.db_path)
        try:
            akun = conn.execute(
                "SELECT username, role, doctor_id FROM users WHERE id = ?",
                (account_id,),
            ).fetchone()
        finally:
            conn.close()

        self.assertEqual(akun["username"], "dokter.andi")
        self.assertEqual(akun["role"], "dokter")
        self.assertEqual(akun["doctor_id"], self.doctor_id)

    def test_username_duplikat_ditolak(self):
        self.account_repo.create_doctor_account(
            self.doctor_id, "dokter.andi", "hash-palsu"
        )
        doctor_id_kedua = self.repo.add_doctor(buat_dokter(nama="Budi Santoso"))

        with self.assertRaises(UsernameAlreadyExistsError):
            self.account_repo.create_doctor_account(
                doctor_id_kedua, "DOKTER.ANDI", "hash-palsu"
            )

    def test_dokter_tidak_boleh_punya_dua_akun(self):
        self.account_repo.create_doctor_account(
            self.doctor_id, "dokter.andi", "hash-palsu"
        )

        with self.assertRaises(InvalidAccountDataError):
            self.account_repo.create_doctor_account(
                self.doctor_id, "dokter.andi.lain", "hash-palsu"
            )

    def test_akun_dokter_tidak_ada_ditolak(self):
        with self.assertRaises(DoctorNotFoundError):
            self.account_repo.create_doctor_account(
                9999, "dokter.hantu", "hash-palsu"
            )

    @patch("auth.service.hash_password", return_value="hash-dari-service")
    def test_auth_service_membuat_akun_dokter(self, mock_hash):
        account_id = self.auth_service.create_doctor_account(
            self.doctor_id, "  dokter.andi  ", "password123"
        )

        self.assertGreater(account_id, 0)
        mock_hash.assert_called_once_with("password123")

    def test_auth_service_menolak_dokter_tidak_ada(self):
        with patch("auth.service.hash_password", return_value="hash"):
            with self.assertRaises(DoctorNotFoundError):
                self.auth_service.create_doctor_account(
                    9999, "dokter.hantu", "password123"
                )

    def test_akun_ikut_terhapus_saat_dokter_dihapus(self):
        self.account_repo.create_doctor_account(
            self.doctor_id, "dokter.andi", "hash-palsu"
        )

        self.repo.delete_doctor(self.doctor_id)

        self.assertEqual(self._hitung_akun(), 0)


if __name__ == "__main__":
    unittest.main()
