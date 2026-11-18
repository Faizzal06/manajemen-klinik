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
        st.info("Form registrasi pasien siap diimplementasikan.")
        # TODO (Anggota 2):
        # - Form username, password, konfirmasi password, nama, alamat,
        #   no_telepon, tanggal_lahir, dan jenis_kelamin.
        # - Panggil auth_service.register_patient(...).
        # - Tangani UsernameAlreadyExistsError / InvalidAccountDataError.
        # - Setelah berhasil, arahkan pasien ke halaman login atau auto-login.
