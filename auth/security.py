from config import MIN_PASSWORD_LENGTH


def hash_password(password: str) -> str:
    """Membuat hash PBKDF2-HMAC-SHA256 dengan salt acak.

    Format yang direncanakan:
    ``pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>``
    """
    # TODO (Anggota 1): Gunakan hashlib.pbkdf2_hmac dan secrets.token_bytes
    pass


def verify_password(password: str, stored_hash: str) -> bool:
    """Memverifikasi password terhadap hash tersimpan secara aman."""
    # TODO (Anggota 1): Parse format hash, hitung ulang, bandingkan dengan hmac.compare_digest
    pass


def validate_username(username: str) -> None:
    """Validasi username: 3-30 karakter, hanya huruf, angka, titik, dan underscore."""
    # TODO (Anggota 1): Raise InvalidAccountDataError jika tidak valid
    pass


def validate_password(password: str) -> None:
    """Validasi panjang password minimal MIN_PASSWORD_LENGTH karakter."""
    # TODO (Anggota 1): Raise InvalidAccountDataError jika terlalu pendek
    pass
