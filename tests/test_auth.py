import unittest


class TestAuthService(unittest.TestCase):
    """Skeleton pengujian autentikasi (Anggota 1)."""

    def test_hash_password_dan_verifikasi(self):
        # TODO: Uji hash_password() dan verify_password().
        pass

    def test_seed_admin_default(self):
        # TODO: Uji ensure_default_admin() hanya membuat satu akun admin.
        pass

    def test_login_berhasil(self):
        # TODO: Uji login dengan kredensial yang benar.
        pass

    def test_login_password_salah(self):
        # TODO: Uji AuthenticationError saat password salah.
        pass

    def test_login_akun_nonaktif(self):
        # TODO: Uji akun dengan is_active = 0 tidak dapat login.
        pass

    def test_registrasi_pasien_membuat_no_rm(self):
        # TODO: Uji registrasi pasien dan pembuatan no_rm otomatis.
        pass

    def test_username_duplikat_ditolak(self):
        # TODO: Uji UsernameAlreadyExistsError.
        pass


if __name__ == "__main__":
    unittest.main()
