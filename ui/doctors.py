import streamlit as st

from auth import AuthService
from database import ClinicRepository
from models import Doctor

_FLASH_KEY = "doctors_flash"


def _show_flash() -> None:
    message = st.session_state.pop(_FLASH_KEY, None)
    if message:
        st.success(message)


def _set_flash(message: str) -> None:
    st.session_state[_FLASH_KEY] = message


def _doctor_label(doctor: Doctor) -> str:
    return f"{doctor.nama} — {doctor.spesialisasi}"


def _show_error(aksi: str, exc: Exception) -> None:
    st.error(f"Gagal {aksi}: {exc}")


def _render_add_form(repo: ClinicRepository) -> None:
    with st.form("form_tambah_dokter", clear_on_submit=True):
        nama = st.text_input("Nama lengkap *")
        kolom_kiri, kolom_kanan = st.columns(2)
        spesialisasi = kolom_kiri.text_input(
            "Spesialisasi *", placeholder="Umum, Anak, Penyakit Dalam, ..."
        )
        no_telepon = kolom_kanan.text_input("No. Telepon")
        alamat = st.text_area("Alamat", height=80)
        jadwal_praktik = st.text_input(
            "Jadwal praktik *", placeholder="Senin - Jumat, 08.00 - 12.00"
        )
        submitted = st.form_submit_button("Simpan Dokter", type="primary")

    if not submitted:
        return

    try:
        dokter = Doctor(
            doctor_id=None,
            nama=nama.strip(),
            alamat=alamat.strip(),
            no_telepon=no_telepon.strip(),
            spesialisasi=spesialisasi,
            jadwal_praktik=jadwal_praktik,
        )
        repo.add_doctor(dokter)
    except Exception as exc:
        _show_error("menyimpan dokter", exc)
    else:
        _set_flash(f"Data dokter {dokter.nama} berhasil disimpan.")
        st.rerun()


def _render_edit_and_delete(
    repo: ClinicRepository, doctors: list[Doctor]
) -> None:
    opsi_dokter = {dokter.id: dokter for dokter in doctors}
    pilihan_id = st.selectbox(
        "Pilih dokter",
        options=list(opsi_dokter),
        format_func=lambda doctor_id: _doctor_label(opsi_dokter[doctor_id]),
        key="doctor_edit_select",
    )
    pilihan = opsi_dokter[pilihan_id]

    with st.form(f"form_edit_dokter_{pilihan.id}"):
        nama = st.text_input("Nama lengkap *", value=pilihan.nama)
        kolom_kiri, kolom_kanan = st.columns(2)
        spesialisasi = kolom_kiri.text_input(
            "Spesialisasi *", value=pilihan.spesialisasi
        )
        no_telepon = kolom_kanan.text_input(
            "No. Telepon", value=pilihan.no_telepon
        )
        alamat = st.text_area("Alamat", value=pilihan.alamat, height=80)
        jadwal_praktik = st.text_input(
            "Jadwal praktik *", value=pilihan.jadwal_praktik
        )
        submitted = st.form_submit_button("Simpan Perubahan", type="primary")

    if submitted:
        try:
            dokter = Doctor(
                doctor_id=pilihan.id,
                nama=nama.strip(),
                alamat=alamat.strip(),
                no_telepon=no_telepon.strip(),
                spesialisasi=spesialisasi,
                jadwal_praktik=jadwal_praktik,
            )
            repo.update_doctor(dokter)
        except Exception as exc:
            _show_error("memperbarui dokter", exc)
        else:
            _set_flash(f"Data dokter {dokter.nama} berhasil diperbarui.")
            st.rerun()

    st.divider()
    with st.expander("Hapus dokter"):
        st.warning(
            "Menghapus data dokter juga menghapus akun login dokter tersebut "
            "beserta seluruh janji yang terkait."
        )
        konfirmasi = st.checkbox(
            f"Saya yakin ingin menghapus {pilihan.nama}.",
            key=f"confirm_delete_doctor_{pilihan.id}",
        )
        if st.button(
            "Hapus Dokter",
            disabled=not konfirmasi,
            key=f"delete_doctor_{pilihan.id}",
        ):
            try:
                repo.delete_doctor(pilihan.id)
            except Exception as exc:
                _show_error("menghapus dokter", exc)
            else:
                _set_flash(f"Data dokter {pilihan.nama} berhasil dihapus.")
                st.rerun()


def _render_doctor_account_form(
    auth_service: AuthService, doctors: list[Doctor]
) -> None:
    st.caption(
        "Akun login dipakai dokter untuk masuk ke aplikasi. Satu dokter "
        "hanya dapat memiliki satu akun."
    )
    opsi_dokter = {dokter.id: dokter for dokter in doctors}
    pilihan_id = st.selectbox(
        "Pilih dokter",
        options=list(opsi_dokter),
        format_func=lambda doctor_id: _doctor_label(opsi_dokter[doctor_id]),
        key="doctor_account_select",
    )
    pilihan = opsi_dokter[pilihan_id]

    with st.form("form_akun_dokter", clear_on_submit=True):
        username = st.text_input("Username *", placeholder="3-30 karakter")
        password = st.text_input(
            "Password awal *", type="password", placeholder="Minimal 8 karakter"
        )
        submitted = st.form_submit_button("Buat Akun Login", type="primary")

    if not submitted:
        return

    try:
        auth_service.create_doctor_account(pilihan.id, username, password)
    except Exception as exc:
        _show_error("membuat akun dokter", exc)
    else:
        _set_flash(f"Akun login untuk {pilihan.nama} berhasil dibuat.")
        st.rerun()


def render_doctors_page(
    repo: ClinicRepository, auth_service: AuthService
) -> None:
    st.header("🩺 Manajemen Dokter")
    st.caption("Kelola data dokter, jadwal praktik, dan akun login dokter.")
    _show_flash()

    try:
        doctors = repo.get_all_doctors() or []
    except Exception as exc:
        _show_error("memuat daftar dokter", exc)
        return

    kolom_total, kolom_spesialisasi = st.columns(2)
    kolom_total.metric("Total Dokter", len(doctors))
    kolom_spesialisasi.metric(
        "Spesialisasi", len({dokter.spesialisasi for dokter in doctors})
    )

    tab_daftar, tab_tambah, tab_edit, tab_akun = st.tabs(
        ["Daftar Dokter", "Tambah Dokter", "Edit / Hapus", "Akun Login"]
    )

    with tab_daftar:
        if not doctors:
            st.info("Belum ada data dokter. Tambahkan dokter melalui tab Tambah Dokter.")
        else:
            st.dataframe(
                [
                    {
                        "Nama": dokter.nama,
                        "Spesialisasi": dokter.spesialisasi,
                        "Jadwal Praktik": dokter.jadwal_praktik,
                        "No. Telepon": dokter.no_telepon,
                        "Alamat": dokter.alamat,
                    }
                    for dokter in doctors
                ],
                use_container_width=True,
                hide_index=True,
            )

    with tab_tambah:
        _render_add_form(repo)

    with tab_edit:
        if not doctors:
            st.info("Belum ada data dokter yang dapat diedit.")
        else:
            _render_edit_and_delete(repo, doctors)

    with tab_akun:
        if not doctors:
            st.info("Tambahkan data dokter terlebih dahulu sebelum membuat akun.")
        else:
            _render_doctor_account_form(auth_service, doctors)
