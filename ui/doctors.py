import streamlit as st
from database import ClinicRepository


def render_doctors_page(repo: ClinicRepository) -> None:
    st.header("🩺 Manajemen Dokter")
    # TODO (Anggota 3): Buat form tambah dokter, daftar spesialisasi & jadwal praktik, serta edit & hapus
    st.info("Halaman Manajemen Dokter siap diimplementasikan.")