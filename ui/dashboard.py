import streamlit as st
from database import ClinicRepository


def render_dashboard(repo: ClinicRepository) -> None:
    st.header("📊 Dashboard Klinik")
    # TODO (Anggota 1): Ambil total pasien, dokter, dan janji dari repo, lalu tampilkan dengan st.metric
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pasien", 0)
    col2.metric("Total Dokter", 0)
    col3.metric("Janji Aktif", 0)