MQTT subscriber: receives JSON from broker, writes daily CSV and inserts into SQLite.
"""

import os, json, csv, time, logging
from datetime import datetime
import sqlite3
import paho.mqtt.client as mqtt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = ROOT / "data" / "raw"
DB_DIR = ROOT / "data" / "database"
RAW_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)

BROKER = os.getenv("MQTT_BROKER", "pf-eveoxy0ua6xhtbdyohag.cedalo.cloud")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("MQTT_TOPIC", "u12345/plant/readings")
CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "plant-subscriber-001")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")

CSV_PATH = RAW_DIR / f"readings_{datetime.utcnow().date()}.csv"
DB_PATH = DB_DIR / "plant_data.sqlite"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# ensure CSV header exists
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
    # CSV
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

    # DB
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        c = conn.cursor()
        c.execute("""
            INSERT INTO readings (timestamp, temperature, humidity, voc, pressure, experiment_id)
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

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT broker")
        client.subscribe(TOPIC)
        logging.info(f"Subscribed to {TOPIC}")
    else:
        logging.error(f"MQTT connect failed rc={rc}")

def on_message(client, userdata, msg):
    ts_iso = datetime.utcnow().isoformat() + "Z"
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
    except Exception:
        logging.exception("Failed to parse MQTT payload")
        return
    payload.setdefault("device_id", "unknown-device")
    payload.setdefault("experiment_id", "unknown-experiment")
    save(ts_iso, payload)
    logging.info(f"Saved reading at {ts_iso}")

def main():
    client = mqtt.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    if MQTT_USER and MQTT_PASS:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    while True:
        try:
            client.connect(BROKER, PORT, 60)
            client.loop_forever()
        except Exception:
            logging.exception("MQTT connection error — retrying in 10s")
            time.sleep(10)

if __name__ == "__main__":
    main()
