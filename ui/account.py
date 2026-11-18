import streamlit as st

from auth import AuthService
from models import Account


def render_account_page(account: Account, auth_service: AuthService) -> None:
    st.header("👤 Akun Saya")

    col1, col2 = st.columns(2)
    col1.text_input("Username", value=account.username, disabled=True)
    col2.text_input("Role", value=account.get_role_label(), disabled=True)

    st.subheader("Ganti Password")
    st.info("Form ganti password siap diimplementasikan.")
    # TODO (Anggota 1):
    # - Form password lama, password baru, dan konfirmasi password baru.
    # - Panggil auth_service.change_password(...).
    # - Tangani AuthenticationError / InvalidAccountDataError.
