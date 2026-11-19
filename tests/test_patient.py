import os
import sys
import tempfile
import types
import unittest
from datetime import date, timedelta
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
    DuplicateMedicalRecordError,
    InvalidAccountDataError,
    PatientNotFoundError,
    UsernameAlreadyExistsError,
)
from models import Patient, PatientAccount, Person


def buat_pasien(**perubahan) -> Patient:
    """Membuat objek Patient dengan data valid sebagai dasar pengujian."""
    data = {
        "patient_id": None,
        "no_rm": "RM-0001",
        "nama": "Budi Santoso",
        "alamat": "Jl. Melati No. 2",
        "no_telepon": "081234567891",
        "tanggal_lahir": "2000-01-01",
        "jenis_kelamin": "Laki-laki",
    }
    data.update(perubahan)
    return Patient(**data)


def geser_tahun(tanggal: date, selisih: int) -> date:
    """Menggeser tahun tanggal, dengan fallback 28 Februari untuk 29 Februari."""
    try:
        return tanggal.replace(year=tanggal.year + selisih)
    except ValueError:
        return tanggal.replace(year=tanggal.year + selisih, day=28)


class TestPatient(unittest.TestCase):
    """Pengujian class Patient (Anggota 2)."""

    def test_patient_mewarisi_person(self):
        pasien = buat_pasien()

        self.assertIsInstance(pasien, Person)
        self.assertIsInstance(pasien, Patient)

    def test_get_role_pasien(self):
        self.assertEqual(buat_pasien().get_role(), "Pasien")

    def test_get_info_pasien(self):
        pasien = buat_pasien()
        umur = date.today().year - 2000

        self.assertEqual(
            pasien.get_info(),
            f"[RM-0001] Budi Santoso (Laki-laki, {umur} tahun)",
        )

    def test_no_rm_dirapikan(self):
        pasien = buat_pasien(no_rm="  rm-0007  ")

        self.assertEqual(pasien.no_rm, "RM-0007")

    def test_no_rm_nomor_besar_diterima(self):
        pasien = buat_pasien(no_rm="RM-10000")

        self.assertEqual(pasien.no_rm, "RM-10000")

    def test_no_rm_tidak_valid_ditolak(self):
        for no_rm in ("0001", "RM-1", "RM-ABCD", "RM-0000", "", None):
            with self.subTest(no_rm=no_rm):
                with self.assertRaises(ValueError):
                    buat_pasien(no_rm=no_rm)

    def test_setter_no_rm_tidak_valid_ditolak(self):
        pasien = buat_pasien()

        with self.assertRaises(ValueError):
            pasien.no_rm = "12345"

    def test_jenis_kelamin_dirapikan(self):
        pasien = buat_pasien(jenis_kelamin="  perempuan ")

        self.assertEqual(pasien.jenis_kelamin, "Perempuan")

    def test_jenis_kelamin_tidak_valid_ditolak(self):
        for jenis_kelamin in ("Lainnya", "L", "", None):
            with self.subTest(jenis_kelamin=jenis_kelamin):
                with self.assertRaises(ValueError):
                    buat_pasien(jenis_kelamin=jenis_kelamin)

    def test_setter_jenis_kelamin_tidak_valid_ditolak(self):
        pasien = buat_pasien()

        with self.assertRaises(ValueError):
            pasien.jenis_kelamin = "Tidak diketahui"

    def test_tanggal_lahir_dinormalisasi(self):
        pasien = buat_pasien(tanggal_lahir="2000-02-29")

        self.assertEqual(pasien.tanggal_lahir, "2000-02-29")

    def test_tanggal_lahir_tidak_valid_ditolak(self):
        for tanggal_lahir in ("01-01-2000", "2000-13-01", "", None):
            with self.subTest(tanggal_lahir=tanggal_lahir):
                with self.assertRaises(ValueError):
                    buat_pasien(tanggal_lahir=tanggal_lahir)

    def test_tanggal_lahir_masa_depan_ditolak(self):
        besok = date.today() + timedelta(days=1)

        with self.assertRaises(ValueError):
            buat_pasien(tanggal_lahir=besok.isoformat())

    def test_hitung_umur_ulang_tahun_sudah_lewat(self):
        hari_ini = date.today()
        lahir = geser_tahun(hari_ini, -25) - timedelta(days=1)

        pasien = buat_pasien(tanggal_lahir=lahir.isoformat())

        self.assertEqual(pasien.hitung_umur(), 25)

    def test_hitung_umur_ulang_tahun_belum_lewat(self):
        hari_ini = date.today()
        lahir = geser_tahun(hari_ini, -25) + timedelta(days=1)

        pasien = buat_pasien(tanggal_lahir=lahir.isoformat())

        self.assertEqual(pasien.hitung_umur(), 24)

    def test_hitung_umur_ulang_tahun_hari_ini(self):
        hari_ini = date.today()
        lahir = geser_tahun(hari_ini, -30)

        pasien = buat_pasien(tanggal_lahir=lahir.isoformat())

        self.assertEqual(pasien.hitung_umur(), 30)

    def test_hitung_umur_29_februari(self):
        pasien = buat_pasien(tanggal_lahir="2000-02-29")
        hari_ini = date.today()
        umur = hari_ini.year - 2000
        if (hari_ini.month, hari_ini.day) < (2, 29):
            umur -= 1

        self.assertEqual(pasien.hitung_umur(), umur)


class TestPatientRepository(unittest.TestCase):
    """Pengujian CRUD pasien pada ClinicRepository (Anggota 2)."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = os.path.join(self.temp_dir.name, "test_clinic.db")
        init_db(self.db_path)
        self.repo = ClinicRepository(self.db_path)

    def test_tambah_dan_ambil_pasien(self):
        pasien = buat_pasien()

        patient_id = self.repo.add_patient(pasien)

        self.assertIsInstance(patient_id, int)
        self.assertGreater(patient_id, 0)
        self.assertEqual(pasien.id, patient_id)

        tersimpan = self.repo.get_patient_by_id(patient_id)
        self.assertEqual(tersimpan.no_rm, "RM-0001")
        self.assertEqual(tersimpan.nama, "Budi Santoso")
        self.assertEqual(tersimpan.jenis_kelamin, "Laki-laki")
        self.assertEqual(tersimpan.tanggal_lahir, "2000-01-01")
        self.assertEqual(tersimpan.alamat, "Jl. Melati No. 2")
        self.assertEqual(tersimpan.no_telepon, "081234567891")

    def test_ambil_pasien_berdasarkan_no_rm(self):
        self.repo.add_patient(buat_pasien())

        tersimpan = self.repo.get_patient_by_no_rm("rm-0001")

        self.assertEqual(tersimpan.nama, "Budi Santoso")

    def test_get_all_patients_urut_nama(self):
        self.repo.add_patient(buat_pasien(no_rm="RM-0001", nama="Budi Santoso"))
        self.repo.add_patient(buat_pasien(no_rm="RM-0002", nama="Ani Lestari"))

        daftar = self.repo.get_all_patients()

        self.assertEqual(
            [pasien.nama for pasien in daftar],
            ["Ani Lestari", "Budi Santoso"],
        )

    def test_pencarian_pasien_berdasarkan_nama_dan_no_rm(self):
        self.repo.add_patient(buat_pasien(no_rm="RM-0001", nama="Budi Santoso"))
        self.repo.add_patient(buat_pasien(no_rm="RM-0002", nama="Ani Lestari"))

        self.assertEqual(
            [pasien.nama for pasien in self.repo.get_all_patients("ani")],
            ["Ani Lestari"],
        )
        self.assertEqual(
            [pasien.nama for pasien in self.repo.get_all_patients("rm-0002")],
            ["Ani Lestari"],
        )
        self.assertEqual(self.repo.get_all_patients("tidak ada"), [])

    def test_next_no_rm(self):
        self.assertEqual(self.repo.next_no_rm(), "RM-0001")

        self.repo.add_patient(buat_pasien(no_rm="RM-0001"))
        self.assertEqual(self.repo.next_no_rm(), "RM-0002")

        self.repo.add_patient(
            buat_pasien(no_rm="RM-0009", nama="Ani Lestari")
        )
        self.assertEqual(self.repo.next_no_rm(), "RM-0010")

    def test_no_rm_duplikat_ditolak(self):
        self.repo.add_patient(buat_pasien())

        with self.assertRaises(DuplicateMedicalRecordError):
            self.repo.add_patient(buat_pasien(nama="Ani Lestari"))

    def test_update_pasien(self):
        patient_id = self.repo.add_patient(buat_pasien())
        pasien = self.repo.get_patient_by_id(patient_id)
        pasien.nama = "Budi Santoso Baru"
        pasien.jenis_kelamin = "Perempuan"
        pasien.no_telepon = "089999999999"

        self.repo.update_patient(pasien)

        diperbarui = self.repo.get_patient_by_id(patient_id)
        self.assertEqual(diperbarui.nama, "Budi Santoso Baru")
        self.assertEqual(diperbarui.jenis_kelamin, "Perempuan")
        self.assertEqual(diperbarui.no_telepon, "089999999999")

    def test_update_no_rm_duplikat_ditolak(self):
        self.repo.add_patient(buat_pasien(no_rm="RM-0001"))
        patient_id = self.repo.add_patient(
            buat_pasien(no_rm="RM-0002", nama="Ani Lestari")
        )
        pasien = self.repo.get_patient_by_id(patient_id)
        pasien.no_rm = "RM-0001"

        with self.assertRaises(DuplicateMedicalRecordError):
            self.repo.update_patient(pasien)

    def test_ambil_pasien_tidak_ditemukan(self):
        with self.assertRaises(PatientNotFoundError):
            self.repo.get_patient_by_id(9999)
        with self.assertRaises(PatientNotFoundError):
            self.repo.get_patient_by_no_rm("RM-9999")

    def test_update_pasien_tidak_ditemukan(self):
        pasien = buat_pasien(patient_id=9999)

        with self.assertRaises(PatientNotFoundError):
            self.repo.update_patient(pasien)

    def test_delete_pasien(self):
        patient_id = self.repo.add_patient(buat_pasien())

        self.repo.delete_patient(patient_id)

        with self.assertRaises(PatientNotFoundError):
            self.repo.get_patient_by_id(patient_id)
        with self.assertRaises(PatientNotFoundError):
            self.repo.delete_patient(patient_id)


class TestPatientAccount(unittest.TestCase):
    """Pengujian akun pasien dan registrasi mandiri (Anggota 2)."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = os.path.join(self.temp_dir.name, "test_clinic.db")
        init_db(self.db_path)
        self.repo = ClinicRepository(self.db_path)
        self.account_repo = AccountRepository(self.db_path)
        self.auth_service = AuthService(self.account_repo, self.repo)
        self.patient_id = self.repo.add_patient(buat_pasien())

    def _hitung(self, tabel: str) -> int:
        conn = get_connection(self.db_path)
        try:
            return conn.execute(f"SELECT COUNT(*) FROM {tabel}").fetchone()[0]
        finally:
            conn.close()

    def test_create_patient_account_di_repository(self):
        account_id = self.account_repo.create_patient_account(
            self.patient_id, "budi.santoso", "hash-palsu"
        )

        self.assertGreater(account_id, 0)
        conn = get_connection(self.db_path)
        try:
            akun = conn.execute(
                "SELECT username, role, patient_id FROM users WHERE id = ?",
                (account_id,),
            ).fetchone()
        finally:
            conn.close()

        self.assertEqual(akun["username"], "budi.santoso")
        self.assertEqual(akun["role"], "pasien")
        self.assertEqual(akun["patient_id"], self.patient_id)

    def test_username_duplikat_ditolak(self):
        self.account_repo.create_patient_account(
            self.patient_id, "budi.santoso", "hash-palsu"
        )
        patient_id_kedua = self.repo.add_patient(
            buat_pasien(no_rm="RM-0002", nama="Ani Lestari")
        )

        with self.assertRaises(UsernameAlreadyExistsError):
            self.account_repo.create_patient_account(
                patient_id_kedua, "BUDI.SANTOSO", "hash-palsu"
            )

    def test_pasien_tidak_boleh_punya_dua_akun(self):
        self.account_repo.create_patient_account(
            self.patient_id, "budi.santoso", "hash-palsu"
        )

        with self.assertRaises(InvalidAccountDataError):
            self.account_repo.create_patient_account(
                self.patient_id, "budi.lain", "hash-palsu"
            )

    def test_akun_pasien_tidak_ada_ditolak(self):
        with self.assertRaises(PatientNotFoundError):
            self.account_repo.create_patient_account(
                9999, "pasien.hantu", "hash-palsu"
            )

    def test_akun_ikut_terhapus_saat_pasien_dihapus(self):
        self.account_repo.create_patient_account(
            self.patient_id, "budi.santoso", "hash-palsu"
        )

        self.repo.delete_patient(self.patient_id)

        self.assertEqual(self._hitung("users"), 0)

    @patch("auth.service.hash_password", return_value="hash-dari-service")
    def test_register_patient_membuat_pasien_dan_akun(self, mock_hash):
        akun = self.auth_service.register_patient(
            username="budi.santoso",
            password="rahasia123",
            nama="Budi Santoso",
            alamat="Jl. Melati No. 2",
            no_telepon="081234567891",
            tanggal_lahir="2000-01-01",
            jenis_kelamin="Laki-laki",
        )

        self.assertIsInstance(akun, PatientAccount)
        self.assertEqual(akun.username, "budi.santoso")
        self.assertEqual(akun.nama, "Budi Santoso")
        self.assertGreater(akun.patient_id, 0)
        mock_hash.assert_called_once_with("rahasia123")

        pasien = self.repo.get_patient_by_id(akun.patient_id)
        self.assertEqual(pasien.no_rm, "RM-0002")
        self.assertEqual(pasien.nama, "Budi Santoso")
        self.assertEqual(self._hitung("users"), 1)

    @patch("auth.service.hash_password", return_value="hash")
    def test_register_patient_no_rm_berurutan(self, _mock_hash):
        pertama = self.auth_service.register_patient(
            "ani.lestari",
            "rahasia123",
            "Ani Lestari",
            "",
            "",
            "2001-02-03",
            "Perempuan",
        )
        kedua = self.auth_service.register_patient(
            "citra.dewi",
            "rahasia123",
            "Citra Dewi",
            "",
            "",
            "2002-03-04",
            "Perempuan",
        )

        self.assertEqual(
            self.repo.get_patient_by_id(pertama.patient_id).no_rm, "RM-0002"
        )
        self.assertEqual(
            self.repo.get_patient_by_id(kedua.patient_id).no_rm, "RM-0003"
        )

    @patch("auth.service.hash_password", return_value="hash")
    def test_register_patient_username_duplikat_rollback(self, _mock_hash):
        self.auth_service.register_patient(
            "budi.santoso",
            "rahasia123",
            "Budi Santoso",
            "",
            "",
            "2000-01-01",
            "Laki-laki",
        )

        with self.assertRaises(UsernameAlreadyExistsError):
            self.auth_service.register_patient(
                "budi.santoso",
                "rahasia123",
                "Budi Lain",
                "",
                "",
                "2000-01-01",
                "Laki-laki",
            )

        self.assertEqual(self._hitung("patients"), 2)
        self.assertEqual(self._hitung("users"), 1)

    @patch("auth.service.hash_password", return_value="hash")
    def test_register_patient_rollback_jika_akun_gagal(self, _mock_hash):
        with patch.object(
            AccountRepository,
            "create_patient_account",
            side_effect=InvalidAccountDataError("gagal membuat akun"),
        ):
            with self.assertRaises(InvalidAccountDataError):
                self.auth_service.register_patient(
                    "budi.santoso",
                    "rahasia123",
                    "Budi Santoso",
                    "",
                    "",
                    "2000-01-01",
                    "Laki-laki",
                )

        self.assertEqual(self._hitung("patients"), 1)
        self.assertEqual(self._hitung("users"), 0)

    def test_register_patient_data_tidak_valid_ditolak(self):
        with patch("auth.service.hash_password", return_value="hash"):
            with self.assertRaises(ValueError):
                self.auth_service.register_patient(
                    "budi.santoso",
                    "rahasia123",
                    "Budi Santoso",
                    "",
                    "",
                    "2000-01-01",
                    "Lainnya",
                )
            with self.assertRaises(ValueError):
                self.auth_service.register_patient(
                    "budi.santoso",
                    "rahasia123",
                    "",
                    "",
                    "",
                    "2000-01-01",
                    "Laki-laki",
                )

        self.assertEqual(self._hitung("patients"), 1)
        self.assertEqual(self._hitung("users"), 0)


if __name__ == "__main__":
    unittest.main()
