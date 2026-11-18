"""Konfigurasi global Sistem Manajemen Klinik."""

APP_NAME = "Sistem Manajemen Klinik"

# --- Autentikasi ---
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"  # TODO: wajib diganti sebelum presentasi
MIN_PASSWORD_LENGTH = 8
SESSION_KEY = "account_id"

# --- Janji Temu ---
CLINIC_OPEN_HOUR = 8
CLINIC_CLOSE_HOUR = 17
SLOT_INTERVAL_MINUTES = 30
BOOKING_DAYS_AHEAD = 30
