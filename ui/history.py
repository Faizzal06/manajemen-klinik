import streamlit as st
from database import ClinicRepository


def render_history_page(repo: ClinicRepository) -> None:
    st.header("📋 Riwayat Kunjungan Pasien")
    # TODO (Anggota 4): Dropdown pilih pasien -> tampilkan daftar riwayat diagnosis & tindakan pasien tersebut
    st.info("Halaman Riwayat Kunjungan siap diimplementasikan.")