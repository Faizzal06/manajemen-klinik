import streamlit as st

from database import ClinicRepository
from models import PatientAccount


def render_patient_dashboard(repo: ClinicRepository, account: PatientAccount) -> None:
    st.header(f"🏠 Dashboard Pasien — {account.nama}")

    # TODO (Anggota 2): Tampilkan ringkasan jumlah janji aktif, kunjungan selesai,
    # dan dokter tersedia menggunakan st.metric.

    tab_booking, tab_janji, tab_riwayat = st.tabs(
        ["📅 Buat Janji Temu", "🗓️ Janji Saya", "📋 Riwayat Saya"]
    )

    with tab_booking:
        st.info("Form booking janji temu siap diimplementasikan.")
        # TODO (Anggota 2 & 4):
        # - Pilih dokter (tampilkan spesialisasi dan jadwal praktik).
        # - Pilih tanggal (mulai hari ini, maksimal BOOKING_DAYS_AHEAD).
        # - Tampilkan slot waktu dari config.py yang belum terisi.
        # - Isi keluhan, lalu panggil repo.create_appointment(...).
        # - Tangani AppointmentConflictError dan tampilkan pesan yang jelas.

    with tab_janji:
        st.info("Daftar janji pasien siap diimplementasikan.")
        # TODO (Anggota 2 & 4):
        # - Tampilkan janji milik account.patient_id.
        # - Sediakan tombol batalkan untuk status 'Terjadwal' yang belum lewat.
        # - Panggil repo.cancel_appointment(...) setelah konfirmasi.

    with tab_riwayat:
        st.info("Riwayat kunjungan pasien siap diimplementasikan.")
        # TODO (Anggota 4):
        # - Tampilkan janji berstatus 'Selesai' milik pasien.
        # - Tampilkan tanggal, dokter, keluhan, diagnosis, dan tindakan.
