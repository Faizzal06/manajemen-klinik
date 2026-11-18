import streamlit as st

from auth import AuthService, get_current_account, logout
from database import AccountRepository, ClinicRepository, init_db
from models import Account
from ui import (
    render_account_page,
    render_accounts_admin_page,
    render_appointments_page,
    render_dashboard,
    render_doctor_appointments_page,
    render_doctor_dashboard,
    render_doctor_history_page,
    render_doctors_page,
    render_examination_page,
    render_history_page,
    render_login_page,
    render_patient_dashboard,
    render_patients_page,
)


def render_sidebar(account: Account) -> str:
    """Menampilkan identitas pengguna dan menu sesuai role."""
    st.sidebar.title("🏥 Manajemen Klinik")
    st.sidebar.caption(f"{account.get_role_label()} • {account.nama}")

    menu = st.sidebar.radio("Navigasi", account.get_menu_items())

    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    return menu


def render_page(
    menu: str,
    account: Account,
    repo: ClinicRepository,
    auth_service: AuthService,
) -> None:
    """Menjalankan halaman berdasarkan menu yang dipilih."""
    if menu == "Dashboard":
        if account.get_role() == "admin":
            render_dashboard(repo)
        elif account.get_role() == "dokter":
            render_doctor_dashboard(repo, account)
        else:
            render_patient_dashboard(repo, account)
    elif menu == "Manajemen Pasien":
        render_patients_page(repo)
    elif menu == "Manajemen Dokter":
        render_doctors_page(repo, auth_service)
    elif menu == "Janji & Pemeriksaan":
        render_appointments_page(repo)
    elif menu == "Janji Saya":
        render_doctor_appointments_page(repo, account)
    elif menu == "Pemeriksaan":
        render_examination_page(repo, account)
    elif menu == "Riwayat Kunjungan":
        render_history_page(repo)
    elif menu == "Riwayat Pasien":
        render_doctor_history_page(repo, account)
    elif menu == "Manajemen Akun":
        render_accounts_admin_page(account, auth_service)
    elif menu == "Akun Saya":
        render_account_page(account, auth_service)


def main() -> None:
    st.set_page_config(
        page_title="Sistem Manajemen Klinik",
        page_icon="🏥",
        layout="wide",
    )

    # Inisialisasi database saat aplikasi dijalankan
    init_db()
    repo = ClinicRepository()
    account_repo = AccountRepository()
    auth_service = AuthService(account_repo, repo)

    # TODO (Anggota 1): Panggil auth_service.ensure_default_admin() saat pertama kali.
    account = get_current_account(auth_service)
    if account is None:
        render_login_page(auth_service)
        st.stop()

    menu = render_sidebar(account)
    render_page(menu, account, repo, auth_service)


if __name__ == "__main__":
    main()
