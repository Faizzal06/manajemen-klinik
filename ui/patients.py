import streamlit as st
from database import ClinicRepository


def render_patients_page(repo: ClinicRepository) -> None:
    st.header("🧑‍⚕️ Manajemen Pasien")
    # TODO (Anggota 2): Buat tab/form tambah pasien, kolom pencarian, tabel data pasien, serta fitur edit & hapus
    st.info("Halaman Manajemen Pasien siap diimplementasikan.")