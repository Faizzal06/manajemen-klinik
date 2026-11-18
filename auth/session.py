import streamlit as st

from config import SESSION_KEY
from models import Account
from .service import AuthService


def set_current_account(account: Account) -> None:
    """Menyimpan ID akun yang sedang login ke session Streamlit."""
    st.session_state[SESSION_KEY] = account.id


def get_current_account(auth_service: AuthService) -> Account | None:
    """Mengambil akun yang sedang login dari session."""
    account_id = st.session_state.get(SESSION_KEY)
    if account_id is None:
        return None

    # TODO (Anggota 1): Muat akun dari database, tangani akun nonaktif,
    # dan bersihkan session jika akun tidak ditemukan.
    return auth_service.get_account(account_id)


def is_authenticated() -> bool:
    """Mengecek apakah session memiliki ID akun."""
    return SESSION_KEY in st.session_state


def logout() -> None:
    """Menghapus sesi login saat ini."""
    st.session_state.pop(SESSION_KEY, None)
