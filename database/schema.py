from .connection import get_connection


def init_db(db_path: str | None = None) -> None:
    """Membuat tabel patients, doctors, appointments, dan users jika belum ada."""
    conn = get_connection(db_path) if db_path else get_connection()
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            no_rm TEXT UNIQUE NOT NULL,
            nama TEXT NOT NULL,
            alamat TEXT,
            no_telepon TEXT,
            tanggal_lahir TEXT,
            jenis_kelamin TEXT
        );

        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            alamat TEXT,
            no_telepon TEXT,
            spesialisasi TEXT NOT NULL,
            jadwal_praktik TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL COLLATE NOCASE UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('admin', 'dokter', 'pasien')),
            patient_id INTEGER UNIQUE REFERENCES patients(id) ON DELETE CASCADE,
            doctor_id INTEGER UNIQUE REFERENCES doctors(id) ON DELETE CASCADE,
            is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CHECK (
                (role = 'admin'  AND patient_id IS NULL     AND doctor_id IS NULL) OR
                (role = 'pasien' AND patient_id IS NOT NULL AND doctor_id IS NULL) OR
                (role = 'dokter' AND doctor_id IS NOT NULL  AND patient_id IS NULL)
            )
        );

        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            tanggal TEXT NOT NULL,
            waktu TEXT NOT NULL,
            keluhan TEXT,
            diagnosis TEXT,
            tindakan TEXT,
            status TEXT DEFAULT 'Terjadwal',
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
        );
        """
    )

    conn.commit()
    conn.close()