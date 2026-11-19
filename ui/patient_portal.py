from datetime import date, datetime, time, timedelta

import streamlit as st

from config import (
    BOOKING_DAYS_AHEAD,
    CLINIC_CLOSE_HOUR,
    CLINIC_OPEN_HOUR,
    SLOT_INTERVAL_MINUTES,
)
from database import ClinicRepository
from exceptions import AppointmentConflictError
from models import Appointment, Patient, PatientAccount


def _show_error(aksi: str, exc: Exception) -> None:
    st.error(f"Gagal {aksi}: {exc}")


def _load_appointments(repo: ClinicRepository, patient_id: int) -> list:
    try:
        return repo.get_appointments_by_patient(patient_id) or []
    except Exception as exc:
        _show_error("memuat janji", exc)
        return []


def _sort_key(appointment) -> tuple[str, str]:
    return (appointment.tanggal, appointment.waktu)


def _doctor_name(appointment) -> str:
    doctor = getattr(appointment, "doctor", None)
    return doctor.nama if doctor is not None else "-"


def _appointment_rows(appointments: list) -> list[dict]:
    return [
        {
            "Tanggal": appointment.tanggal,
            "Waktu": appointment.waktu,
            "Dokter": _doctor_name(appointment),
            "Keluhan": appointment.keluhan or "-",
            "Diagnosis": appointment.diagnosis or "-",
            "Tindakan": appointment.tindakan or "-",
            "Status": appointment.status,
        }
        for appointment in appointments
    ]


def _slot_waktu() -> list[str]:
    """Membuat daftar slot waktu praktik dari konfigurasi klinik."""
    slot = []
    saat_ini = datetime.combine(date.today(), time(CLINIC_OPEN_HOUR, 0))
    batas = datetime.combine(date.today(), time(CLINIC_CLOSE_HOUR, 0))
    while saat_ini < batas:
        slot.append(saat_ini.strftime("%H:%M"))
        saat_ini += timedelta(minutes=SLOT_INTERVAL_MINUTES)
    return slot


def _render_data_diri(patient: Patient) -> None:
    with st.expander("Data Diri"):
        st.markdown(
            f"**No. Rekam Medis:** {patient.no_rm}  \n"
            f"**Nama:** {patient.nama}  \n"
            f"**Tanggal Lahir:** {patient.tanggal_lahir} "
            f"({patient.hitung_umur()} tahun)  \n"
            f"**Jenis Kelamin:** {patient.jenis_kelamin}  \n"
            f"**No. Telepon:** {patient.no_telepon or '-'}  \n"
            f"**Alamat:** {patient.alamat or '-'}"
        )


def _render_booking_tab(repo: ClinicRepository, patient: Patient | None) -> None:
    if patient is None:
        st.info("Data pasien belum tersedia sehingga janji belum dapat dibuat.")
        return

    try:
        doctors = repo.get_all_doctors() or []
    except Exception as exc:
        _show_error("memuat daftar dokter", exc)
        return

    if not doctors:
        st.info("Belum ada dokter yang tersedia.")
        return

    opsi_dokter = {dokter.id: dokter for dokter in doctors}
    pilihan_id = st.selectbox(
        "Pilih dokter",
        options=list(opsi_dokter),
        format_func=lambda doctor_id: (
            f"{opsi_dokter[doctor_id].nama} — "
            f"{opsi_dokter[doctor_id].spesialisasi}"
        ),
        key="patient_booking_doctor",
    )
    dokter = opsi_dokter[pilihan_id]
    st.caption(f"Jadwal praktik: {dokter.jadwal_praktik}")

    tanggal = st.date_input(
        "Tanggal",
        value=date.today(),
        min_value=date.today(),
        max_value=date.today() + timedelta(days=BOOKING_DAYS_AHEAD),
        key="patient_booking_date",
    )

    try:
        waktu_terisi = set(
            repo.get_booked_times(dokter.id, tanggal.isoformat()) or []
        )
    except Exception as exc:
        _show_error("memuat slot waktu", exc)
        waktu_terisi = set()

    slot_tersedia = [
        slot for slot in _slot_waktu() if slot not in waktu_terisi
    ]
    if not slot_tersedia:
        st.warning("Semua slot waktu pada tanggal ini sudah terisi.")
        return

    waktu = st.selectbox(
        "Slot waktu", slot_tersedia, key="patient_booking_time"
    )
    keluhan = st.text_area(
        "Keluhan", height=80, key="patient_booking_complaint"
    )

    if st.button("Simpan Janji Temu", type="primary"):
        try:
            janji = Appointment(
                appointment_id=None,
                patient=patient,
                doctor=dokter,
                tanggal=tanggal.isoformat(),
                waktu=waktu,
                keluhan=keluhan.strip(),
            )
            appointment_id = repo.create_appointment(janji)
        except AppointmentConflictError as exc:
            st.error(f"Jadwal bentrok: {exc}")
        except Exception as exc:
            _show_error("menyimpan janji", exc)
        else:
            if appointment_id is None:
                # create_appointment() masih stub milik Anggota 4.
                st.warning(
                    "Janji belum dapat disimpan karena layanan janji temu "
                    "belum tersedia."
                )
            else:
                st.success(
                    f"Janji dengan {dokter.nama} pada "
                    f"{tanggal.isoformat()} pukul {waktu} berhasil dibuat."
                )
                st.rerun()


def render_patient_dashboard(repo: ClinicRepository, account: PatientAccount) -> None:
    st.header(f"🏠 Dashboard Pasien — {account.nama}")

    try:
        patient = repo.get_patient_by_id(account.patient_id)
    except Exception as exc:
        st.warning(f"Data profil pasien belum dapat dimuat: {exc}")
        patient = None
    else:
        st.caption(patient.get_info())

    appointments = _load_appointments(repo, account.patient_id)
    janji_aktif = [
        appointment for appointment in appointments if appointment.status == "Terjadwal"
    ]
    kunjungan_selesai = [
        appointment for appointment in appointments if appointment.status == "Selesai"
    ]

    try:
        jumlah_dokter = len(repo.get_all_doctors() or [])
    except Exception:
        jumlah_dokter = 0

    kolom_aktif, kolom_selesai, kolom_dokter = st.columns(3)
    kolom_aktif.metric("Janji Aktif", len(janji_aktif))
    kolom_selesai.metric("Kunjungan Selesai", len(kunjungan_selesai))
    kolom_dokter.metric("Dokter Tersedia", jumlah_dokter)

    if patient is not None:
        _render_data_diri(patient)

    tab_booking, tab_janji, tab_riwayat = st.tabs(
        ["📅 Buat Janji Temu", "🗓️ Janji Saya", "📋 Riwayat Saya"]
    )

    with tab_booking:
        _render_booking_tab(repo, patient)

    with tab_janji:
        if not appointments:
            st.info("Belum ada janji temu.")
        else:
            st.dataframe(
                _appointment_rows(sorted(appointments, key=_sort_key)),
                use_container_width=True,
                hide_index=True,
            )

    with tab_riwayat:
        riwayat = sorted(
            [
                appointment
                for appointment in appointments
                if appointment.status == "Selesai"
            ],
            key=_sort_key,
            reverse=True,
        )
        if not riwayat:
            st.info("Belum ada kunjungan yang selesai.")
        else:
            st.dataframe(
                _appointment_rows(riwayat),
                use_container_width=True,
                hide_index=True,
            )
