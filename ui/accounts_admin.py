import streamlit as st

from auth import AuthService
from models import AdminAccount


def render_accounts_admin_page(
    account: AdminAccount, auth_service: AuthService
) -> None:
    st.header("🔑 Manajemen Akun")
    st.info("Daftar akun dan pengelolaan akun siap diimplementasikan.")

    # TODO (Anggota 1):
    # - Tampilkan auth_service / AccountRepository.list_accounts().
    # - Sediakan reset password dan aktivasi/nonaktivasi akun.
    # - Jangan izinkan admin menonaktifkan akunnya sendiri.
    # - Jangan izinkan admin terakhir dinonaktifkan.
