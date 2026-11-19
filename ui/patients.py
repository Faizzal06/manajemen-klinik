from datetime import date

import streamlit as st

from database import ClinicRepository
from models import Patient

_FLASH_KEY = "patients_flash"


def _show_flash() -> None:
    message = st.session_state.pop(_FLASH_KEY, None)
    if message:
        st.success(message)


def _set_flash(message: str) -> None:
    st.session_state[_FLASH_KEY] = message


def _patient_label(patient: Patient) -> str:
    return f"[{patient.no_rm}] {patient.nama}"


def _show_error(aksi: str, exc: Exception) -> None:
    st.error(f"Gagal {aksi}: {exc}")


def _parse_tanggal(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def _render_add_form(repo: ClinicRepository) -> None:
    try:
        no_rm = repo.next_no_rm()
    except Exception as exc:
        _show_error("menyiapkan nomor rekam medis", exc)
        return

    with st.form("form_tambah_pasien", clear_on_submit=True):
        st.text_input("No. Rekam Medis", value=no_rm, disabled=True)
        nama = st.text_input("Nama lengkap *")
        kolom_kiri, kolom_kanan = st.columns(2)
        no_telepon = kolom_kiri.text_input("No. Telepon")
        jenis_kelamin = kolom_kanan.selectbox(
            "Jenis kelamin *", ["Laki-laki", "Perempuan"]
        )
        tanggal_lahir = st.date_input(
            "Tanggal lahir *",
            value=None,
            min_value=date(1900, 1, 1),
            max_value=date.today(),
        )
        alamat = st.text_area("Alamat", height=80)
        submitted = st.form_submit_button("Simpan Pasien", type="primary")

    if not submitted:
        return

    if not nama.strip():
        st.error("Nama pasien wajib diisi.")
        return
    if tanggal_lahir is None:
        st.error("Tanggal lahir wajib diisi.")
        return

    try:
        pasien = Patient(
            patient_id=None,
            no_rm=no_rm,
            nama=nama.strip(),
            alamat=alamat.strip(),
            no_telepon=no_telepon.strip(),
            tanggal_lahir=tanggal_lahir.isoformat(),
            jenis_kelamin=jenis_kelamin,
        )
        repo.add_patient(pasien)
    except Exception as exc:
        _show_error("menyimpan pasien", exc)
    else:
        _set_flash(f"Data pasien {pasien.nama} berhasil disimpan.")
        st.rerun()


def _render_edit_and_delete(
    repo: ClinicRepository, patients: list[Patient]
) -> None:
    opsi_pasien = {pasien.id: pasien for pasien in patients}
    pilihan_id = st.selectbox(
        "Pilih pasien",
        options=list(opsi_pasien),
        format_func=lambda patient_id: _patient_label(opsi_pasien[patient_id]),
        key="patient_edit_select",
    )
    pilihan = opsi_pasien[pilihan_id]

    with st.form(f"form_edit_pasien_{pilihan.id}"):
        st.text_input("No. Rekam Medis", value=pilihan.no_rm, disabled=True)
        nama = st.text_input("Nama lengkap *", value=pilihan.nama)
        kolom_kiri, kolom_kanan = st.columns(2)
        no_telepon = kolom_kiri.text_input(
            "No. Telepon", value=pilihan.no_telepon
        )
        jenis_kelamin = kolom_kanan.selectbox(
            "Jenis kelamin *",
            ["Laki-laki", "Perempuan"],
            index=0 if pilihan.jenis_kelamin == "Laki-laki" else 1,
        )
        tanggal_lahir = st.date_input(
            "Tanggal lahir *",
            value=_parse_tanggal(pilihan.tanggal_lahir),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
        )
        alamat = st.text_area("Alamat", value=pilihan.alamat, height=80)
        submitted = st.form_submit_button("Simpan Perubahan", type="primary")

    if submitted:
        if not nama.strip():
            st.error("Nama pasien wajib diisi.")
        elif tanggal_lahir is None:
            st.error("Tanggal lahir wajib diisi.")
        else:
            try:
                pasien = Patient(
                    patient_id=pilihan.id,
                    no_rm=pilihan.no_rm,
                    nama=nama.strip(),
                    alamat=alamat.strip(),
                    no_telepon=no_telepon.strip(),
                    tanggal_lahir=tanggal_lahir.isoformat(),
                    jenis_kelamin=jenis_kelamin,
                )
                repo.update_patient(pasien)
            except Exception as exc:
                _show_error("memperbarui pasien", exc)
            else:
                _set_flash(f"Data pasien {pasien.nama} berhasil diperbarui.")
                st.rerun()

    st.divider()
    with st.expander("Hapus pasien"):
        st.warning(
            "Menghapus data pasien juga menghapus akun login dan seluruh "
            "janji pemeriksaan yang terkait."
        )
        konfirmasi = st.checkbox(
            f"Saya yakin ingin menghapus {pilihan.nama}.",
            key=f"confirm_delete_patient_{pilihan.id}",
        )
        if st.button(
            "Hapus Pasien",
            disabled=not konfirmasi,
            key=f"delete_patient_{pilihan.id}",
        ):
            try:
                repo.delete_patient(pilihan.id)
            except Exception as exc:
                _show_error("menghapus pasien", exc)
            else:
                _set_flash(f"Data pasien {pilihan.nama} berhasil dihapus.")
                st.rerun()


def render_patients_page(repo: ClinicRepository) -> None:
    st.header("🧑‍⚕️ Manajemen Pasien")
    st.caption(
        "Kelola data pasien. Akun login pasien dibuat mandiri melalui "
        "halaman login (tab Daftar Pasien)."
    )
    _show_flash()

    try:
        patients = repo.get_all_patients() or []
    except Exception as exc:
        _show_error("memuat daftar pasien", exc)
        return

    kolom_total, kolom_laki, kolom_perempuan = st.columns(3)
    kolom_total.metric("Total Pasien", len(patients))
    kolom_laki.metric(
        "Laki-laki",
        sum(1 for pasien in patients if pasien.jenis_kelamin == "Laki-laki"),
    )
    kolom_perempuan.metric(
        "Perempuan",
        sum(1 for pasien in patients if pasien.jenis_kelamin == "Perempuan"),
    )

    tab_daftar, tab_tambah, tab_edit = st.tabs(
        ["Daftar Pasien", "Tambah Pasien", "Edit / Hapus"]
    )

    with tab_daftar:
        keyword = st.text_input(
            "Cari nama atau No. RM", key="patient_search"
        )
        try:
            hasil = repo.get_all_patients(keyword) or []
        except Exception as exc:
            _show_error("mencari pasien", exc)
            return

        if not hasil:
            st.info("Tidak ada data pasien yang cocok.")
        else:
            st.dataframe(
                [
                    {
                        "No. RM": pasien.no_rm,
                        "Nama": pasien.nama,
                        "Jenis Kelamin": pasien.jenis_kelamin,
                        "Tanggal Lahir": pasien.tanggal_lahir,
                        "Umur": pasien.hitung_umur(),
                        "No. Telepon": pasien.no_telepon,
                        "Alamat": pasien.alamat,
                    }
                    for pasien in hasil
                ],
                use_container_width=True,
                hide_index=True,
            )

    with tab_tambah:
        _render_add_form(repo)

    with tab_edit:
        if not patients:
            st.info("Belum ada data pasien yang dapat diedit.")
        else:
            _render_edit_and_delete(repo, patients)
