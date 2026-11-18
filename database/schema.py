from .connection import get_connection


def init_db(db_path: str | None = None) -> None:
    """Membuat tabel patients, doctors, dan appointments jika belum ada."""
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