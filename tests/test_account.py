import unittest


class TestAccount(unittest.TestCase):
    """Skeleton pengujian inheritance dan polymorphism Account (Anggota 1)."""

    def test_role_dan_label_setiap_akun(self):
        # TODO: Uji get_role() dan get_role_label() untuk AdminAccount,
        # DoctorAccount, dan PatientAccount.
        pass

    def test_menu_sidebar_sesuai_role(self):
        # TODO: Uji get_menu_items() setiap subclass Account.
        pass

    def test_hak_akses_berbeda_tiap_role(self):
        # TODO: Uji can_manage_patients(), can_examine(), can_book_for_self().
        pass


if __name__ == "__main__":
    unittest.main()
