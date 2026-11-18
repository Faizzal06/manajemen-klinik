import streamlit as st

from database import ClinicRepository
from models import DoctorAccount


def render_doctor_dashboard(repo: ClinicRepository, account: DoctorAccount) -> None:
    st.header(f"🏠 Dashboard Dokter — {account.nama}")
    # TODO (Anggota 3): Tampilkan janji hari ini, jumlah janji menunggu
    # pemeriksaan, dan jumlah pemeriksaan selesai.


def render_doctor_appointments_page(
    repo: ClinicRepository, account: DoctorAccount
) -> None:
    st.header("🗓️ Janji Saya")
    # TODO (Anggota 3): Tampilkan janji milik account.doctor_id.
    # Sediakan filter tanggal/status dan tombol menuju form pemeriksaan.


def render_examination_page(repo: ClinicRepository, account: DoctorAccount) -> None:
    st.header("🩺 Pemeriksaan")
    st.info("Form pemeriksaan siap diimplementasikan.")
    # TODO (Anggota 4):
    # - Pilih janji berstatus 'Terjadwal' milik dokter yang login.
    # - Tampilkan keluhan pasien.
    # - Form diagnosis dan tindakan, lalu panggil repo.update_examination(...).
    # - Pastikan dokter tidak dapat memeriksa janji milik dokter lain.


def render_doctor_history_page(repo: ClinicRepository, account: DoctorAccount) -> None:
    st.header("📋 Riwayat Pasien")
    # TODO (Anggota 3): Pilih pasien yang pernah ditangani oleh dokter ini,
    # lalu tampilkan riwayat diagnosis dan tindakannya.
