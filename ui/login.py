from datetime import date

import streamlit as st

from auth import AuthService


def render_login_page(auth_service: AuthService) -> None:
    st.header("🔐 Masuk ke Sistem Manajemen Klinik")
    st.caption("Silakan masuk atau daftar sebagai pasien baru.")

    tab_masuk, tab_daftar = st.tabs(["Masuk", "Daftar Pasien"])

    with tab_masuk:
        st.info("Form login siap diimplementasikan.")
        # TODO (Anggota 1):
        # - Form username & password (type="password").
        # - Panggil auth_service.login(username, password).
        # - Tangani AuthenticationError dengan pesan generik.
        # - Simpan akun ke session dengan set_current_account(account), lalu st.rerun().

    with tab_daftar:
        with st.form("form_daftar_pasien", clear_on_submit=True):
            username = st.text_input(
                "Username *", placeholder="3-30 karakter"
            )
            kolom_password, kolom_konfirmasi = st.columns(2)
            password = kolom_password.text_input(
                "Password *",
                type="password",
                placeholder="Minimal 8 karakter",
            )
            konfirmasi = kolom_konfirmasi.text_input(
                "Konfirmasi password *", type="password"
            )
            nama = st.text_input("Nama lengkap *")
            kolom_telepon, kolom_jk = st.columns(2)
            no_telepon = kolom_telepon.text_input("No. Telepon")
            jenis_kelamin = kolom_jk.selectbox(
                "Jenis kelamin *", ["Laki-laki", "Perempuan"]
            )
            tanggal_lahir = st.date_input(
                "Tanggal lahir *",
                value=None,
                min_value=date(1900, 1, 1),
                max_value=date.today(),
            )
            alamat = st.text_area("Alamat", height=80)
            submitted = st.form_submit_button("Daftar", type="primary")

        if submitted:
            if password != konfirmasi:
                st.error("Konfirmasi password tidak cocok.")
            elif tanggal_lahir is None:
                st.error("Tanggal lahir wajib diisi.")
            else:
                try:
                    auth_service.register_patient(
                        username=username,
                        password=password,
                        nama=nama,
                        alamat=alamat,
                        no_telepon=no_telepon,
                        tanggal_lahir=tanggal_lahir.isoformat(),
                        jenis_kelamin=jenis_kelamin,
                    )
                except Exception as exc:
                    st.error(f"Registrasi gagal: {exc}")
                else:
                    st.success(
                        "Registrasi berhasil. Silakan masuk melalui tab Masuk."
                    )
