Serial subscriber: reads JSON lines from the Arduino NICLA (Serial) and stores to CSV + SQLite.
"""

import os, json, csv, time, logging
from datetime import datetime
import sqlite3
import serial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = ROOT / "data" / "raw"
DB_DIR = ROOT / "data" / "database"
RAW_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)

# TODO: set your serial port or export SERIAL_PORT env var
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/tty.usbmodemXXXX")  # change to your port
BAUD = int(os.getenv("SERIAL_BAUD", 115200))

CSV_PATH = RAW_DIR / f"readings_{datetime.utcnow().date()}.csv"
DB_PATH = DB_DIR / "plant_data.sqlite"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

if not CSV_PATH.exists():
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp","temperature","humidity","voc","pressure","device_id","experiment_id","raw_json"])

# init DB
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
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

init_db()

def save(ts_iso, payload):
    # csv
    try:
        with open(CSV_PATH, "a", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                ts_iso,
                payload.get("temperature"),
                payload.get("humidity"),
                payload.get("voc"),
                payload.get("pressure"),
                payload.get("device_id"),
                payload.get("experiment_id"),
                json.dumps(payload)
            ])
    except Exception:
        logging.exception("CSV write failed")
    # db
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        c = conn.cursor()
        c.execute("""
            INSERT INTO readings (timestamp, temperature, humidity, voc, pressure, device_id, experiment_id, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (ts_iso,
              payload.get("temperature"),
              payload.get("humidity"),
              payload.get("voc"),
              payload.get("pressure"),
              payload.get("device_id"),
              payload.get("experiment_id"),

              json.dumps(payload)))
        conn.commit()
        conn.close()
    except Exception:
        logging.exception("DB write failed")

def main():
    logging.info(f"Opening serial port: {SERIAL_PORT} @ {BAUD}")
    while True:
        try:
            with serial.Serial(SERIAL_PORT, BAUD, timeout=2) as ser:
                logging.info("Serial opened")
                while True:
                    line = ser.readline()
                    if not line:
                        continue
                    try:
                        text = line.decode("utf-8").strip()
                        if not text:
                            continue
                        payload = json.loads(text)
                        ts_iso = datetime.utcnow().isoformat() + "Z"
                        payload.setdefault("device_id", "nicla-unknown")
                        payload.setdefault("experiment_id", "unknown-experiment")
                        save(ts_iso, payload)
                        logging.info(f"Saved serial reading {ts_iso}")
                    except json.JSONDecodeError:
                        logging.warning("Non-JSON serial line skipped")
                    except Exception:
                        logging.exception("Error processing serial line")
        except serial.SerialException:
            logging.exception("Serial port error — retrying in 5s")
            time.sleep(5)
        except Exception:
            logging.exception("Unexpected error — retrying in 10s")
            time.sleep(10)

if __name__ == "__main__":
    main()

