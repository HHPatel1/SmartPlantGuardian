
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "data" / "database" / "plant_data.sqlite"

def get_connection():
    return sqlite3.connect(DB)

def create_tables():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        temperature REAL,
        humidity REAL,
        voc REAL,
        pressure REAL,
        device_id TEXT,
        experiment_id TEXT,
        raw_json TEXT
    );
    """)
    conn.commit()
    conn.close()

