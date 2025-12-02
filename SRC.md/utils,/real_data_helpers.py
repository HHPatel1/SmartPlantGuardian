import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load_latest_csv():
    raw_dir = ROOT / "data" / "raw"
    latest = sorted(raw_dir.glob("*.csv"))[-1]
    return pd.read_csv(latest)

