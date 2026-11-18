from datetime import date

import streamlit as st

from database import ClinicRepository
from models import DoctorAccount


def _load_appointments(repo: ClinicRepository, doctor_id: int) -> list:
    try:
        return repo.get_appointments_by_doctor(doctor_id) or []
    except Exception as exc:
        st.error(f"Gagal memuat janji dokter: {exc}")
        return []


def _sort_key(appointment) -> tuple[str, str]:
    return (appointment.tanggal, appointment.waktu)


def _patient_name(appointment) -> str:
    patient = getattr(appointment, "patient", None)
    return patient.nama if patient is not None else "-"


def _format_appointment_label(appointment) -> str:
    return (
        f"{appointment.tanggal} {appointment.waktu} — "
        f"{_patient_name(appointment)} ({appointment.status})"
    )


def _appointment_rows(appointments: list) -> list[dict]:
    return [
        {
            "Tanggal": appointment.tanggal,
            "Waktu": appointment.waktu,
            "Pasien": _patient_name(appointment),
            "Keluhan": appointment.keluhan or "-",
            "Diagnosis": appointment.diagnosis or "-",
            "Tindakan": appointment.tindakan or "-",
            "Status": appointment.status,
        }
        for appointment in appointments
    ]


def render_doctor_dashboard(repo: ClinicRepository, account: DoctorAccount) -> None:
    st.header(f"🏠 Dashboard Dokter — {account.nama}")

    try:
        dokter = repo.get_doctor_by_id(account.doctor_id)
    except Exception as exc:
        st.warning(f"Data profil dokter belum dapat dimuat: {exc}")
    else:
        st.caption(dokter.get_info())

    appointments = _load_appointments(repo, account.doctor_id)
    hari_ini = date.today().isoformat()
    janji_hari_ini = sorted(
        [
            appointment
            for appointment in appointments
            if appointment.tanggal == hari_ini and appointment.status != "Dibatalkan"
        ],
        key=_sort_key,
    )
    menunggu = [
        appointment for appointment in appointments if appointment.status == "Terjadwal"
    ]
    selesai = [
        appointment for appointment in appointments if appointment.status == "Selesai"
    ]

    kolom_hari_ini, kolom_menunggu, kolom_selesai = st.columns(3)
    kolom_hari_ini.metric("Janji Hari Ini", len(janji_hari_ini))
    kolom_menunggu.metric("Menunggu Pemeriksaan", len(menunggu))
    kolom_selesai.metric("Pemeriksaan Selesai", len(selesai))

    st.subheader("Jadwal Hari Ini")
    if not janji_hari_ini:
        st.info("Tidak ada janji pemeriksaan pada hari ini.")
    else:
        st.dataframe(
            _appointment_rows(janji_hari_ini),
            use_container_width=True,
            hide_index=True,
        )


def render_doctor_appointments_page(
    repo: ClinicRepository, account: DoctorAccount
) -> None:
    st.header("🗓️ Janji Saya")
    st.caption(
        "Daftar janji yang ditangani oleh dokter yang sedang login. "
        "Gunakan menu Pemeriksaan untuk mengisi hasil pemeriksaan."
    )

    appointments = _load_appointments(repo, account.doctor_id)
    if not appointments:
        st.info("Belum ada janji untuk dokter ini.")
        return

    appointments = sorted(appointments, key=_sort_key)
    daftar_tanggal = ["Semua"] + sorted(
        {appointment.tanggal for appointment in appointments}, reverse=True
    )
    daftar_status = ["Semua", "Terjadwal", "Selesai", "Dibatalkan"]

    kolom_tanggal, kolom_status = st.columns(2)
    filter_tanggal = kolom_tanggal.selectbox("Filter tanggal", daftar_tanggal)
    filter_status = kolom_status.selectbox("Filter status", daftar_status)

    hasil_filter = [
        appointment
        for appointment in appointments
        if (filter_tanggal == "Semua" or appointment.tanggal == filter_tanggal)
        and (filter_status == "Semua" or appointment.status == filter_status)
    ]

    if not hasil_filter:
        st.info("Tidak ada janji yang sesuai dengan filter.")
        return

    st.dataframe(
        _appointment_rows(hasil_filter),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Detail Janji")
    opsi_janji = {appointment.id: appointment for appointment in hasil_filter}
    pilihan_id = st.selectbox(
        "Pilih janji",
        options=list(opsi_janji),
        format_func=lambda appointment_id: _format_appointment_label(
            opsi_janji[appointment_id]
        ),
        key="doctor_appointment_detail",
    )
    pilihan = opsi_janji[pilihan_id]

    with st.container():
        st.markdown(
            f"**Pasien:** {_patient_name(pilihan)}  \n"
            f"**Jadwal:** {pilihan.tanggal} pukul {pilihan.waktu}  \n"
            f"**Status:** {pilihan.status}  \n"
            f"**Keluhan:** {pilihan.keluhan or '-'}  \n"
            f"**Diagnosis:** {pilihan.diagnosis or '-'}  \n"
            f"**Tindakan:** {pilihan.tindakan or '-'}"
        )

    if pilihan.status != "Terjadwal":
        st.caption("Hanya janji berstatus Terjadwal yang dapat diperiksa.")
        return

    if st.button("Pilih untuk Pemeriksaan", type="primary"):
        st.session_state["selected_appointment_id"] = pilihan.id
        st.success(
            "Janji dipilih. Buka menu **Pemeriksaan** untuk mengisi diagnosis "
            "dan tindakan."
        )


def render_doctor_history_page(repo: ClinicRepository, account: DoctorAccount) -> None:
    st.header("📋 Riwayat Pasien")
    st.caption("Riwayat pemeriksaan pasien yang pernah ditangani oleh dokter ini.")

    appointments = _load_appointments(repo, account.doctor_id)
    riwayat_selesai = [
        appointment for appointment in appointments if appointment.status == "Selesai"
    ]

    pasien_unik: dict[int, object] = {}
    for appointment in riwayat_selesai:
        patient = getattr(appointment, "patient", None)
        if patient is not None:
            pasien_unik[patient.id] = patient

    if not pasien_unik:
        st.info("Belum ada pasien dengan pemeriksaan selesai.")
        return

    pilihan_id = st.selectbox(
        "Pilih pasien",
        options=list(pasien_unik),
        format_func=lambda patient_id: (
            f"{pasien_unik[patient_id].nama} ({pasien_unik[patient_id].no_rm})"
        ),
        key="doctor_history_patient",
    )
    pilihan_pasien = pasien_unik[pilihan_id]

    riwayat_pasien = sorted(
        [
            appointment
            for appointment in riwayat_selesai
            if getattr(appointment, "patient", None) is not None
            and appointment.patient.id == pilihan_pasien.id
        ],
        key=_sort_key,
        reverse=True,
    )

    st.dataframe(
        _appointment_rows(riwayat_pasien),
        use_container_width=True,
        hide_index=True,
    )


def render_examination_page(repo: ClinicRepository, account: DoctorAccount) -> None:
    st.header("🩺 Pemeriksaan")
    st.info("Form pemeriksaan siap diimplementasikan.")
    # TODO (Anggota 4):
    # - Pilih janji berstatus 'Terjadwal' milik dokter yang login.
    # - Tampilkan keluhan pasien.
    # - Form diagnosis dan tindakan, lalu panggil repo.update_examination(...).
    # - Pastikan dokter tidak dapat memeriksa janji milik dokter lain.
