import streamlit as st
from database import ClinicRepository


def render_appointments_page(repo: ClinicRepository) -> None:
    st.header("📅 Janji Temu & Pemeriksaan")
    # TODO (Anggota 4): Buat 2 tab: (1) Buat/Batalkan Janji Temu, (2) Input Hasil Pemeriksaan
    # (Keluhan, Diagnosis, Tindakan).
    # Halaman ini khusus admin: admin dapat membuat janji untuk pasien mana pun.
    # Booking mandiri pasien ada di ui/patient_portal.py.
    st.info("Halaman Janji & Pemeriksaan siap diimplementasikan.")