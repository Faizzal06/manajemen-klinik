import streamlit as st
from database import init_db, ClinicRepository
from ui import (
    render_dashboard,
    render_patients_page,
    render_doctors_page,
    render_appointments_page,
    render_history_page,
)


def main() -> None:
    st.set_page_config(
        page_title="Sistem Manajemen Klinik",
        page_icon="🏥",
        layout="wide",
    )

    # Inisialisasi database saat aplikasi dijalankan
    init_db()
    repo = ClinicRepository()

    st.sidebar.title("🏥 Manajemen Klinik")
    menu = st.sidebar.radio(
        "Navigasi",
        [
            "Dashboard",
            "Manajemen Pasien",
            "Manajemen Dokter",
            "Janji & Pemeriksaan",
            "Riwayat Kunjungan",
        ],
    )

    if menu == "Dashboard":
        render_dashboard(repo)
    elif menu == "Manajemen Pasien":
        render_patients_page(repo)
    elif menu == "Manajemen Dokter":
        render_doctors_page(repo)
    elif menu == "Janji & Pemeriksaan":
        render_appointments_page(repo)
    elif menu == "Riwayat Kunjungan":
        render_history_page(repo)


if __name__ == "__main__":
    main()