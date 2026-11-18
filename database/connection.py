import os
import sqlite3

DB_PATH = os.path.join("data", "clinic.db")


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Membuka koneksi ke database SQLite dengan dukungan foreign key."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn