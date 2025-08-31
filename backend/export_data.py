# backend/export_data.py
import os
import json
import csv
from sqlalchemy.orm import sessionmaker
from backend.database import engine, SessionLocal, Perpetrator, Sighting, init_db

# --- Init DB ---
print("[EXPORT] Initializing DB connection...")
init_db()
session = SessionLocal()
print("[EXPORT] DB ready.")

# --- Paths ---
EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)
JSON_PATH = os.path.join(EXPORT_DIR, "uwsd_data.json")
CSV_PATH = os.path.join(EXPORT_DIR, "uwsd_data.csv")

# --- Export to JSON ---
print("[EXPORT] Exporting to JSON...")
data_json = []

perps = session.query(Perpetrator).all()
for perp in perps:
    perp_dict = {
        "id": perp.id,
        "name": perp.name,
        "fake_ssn": perp.fake_ssn,
        "fake_address": perp.fake_address,
        "threat_level": perp.threat_level,
        "sightings": [
            {
                "id": s.id,
                "timestamp": s.timestamp.isoformat(),
                "location": s.location,
                "screenshot_path": s.screenshot_path
            } for s in perp.sightings
        ]
    }
    data_json.append(perp_dict)

with open(JSON_PATH, "w") as f:
    json.dump(data_json, f, indent=4)

print(f"[EXPORT] JSON exported to {JSON_PATH}")

# --- Export to CSV ---
print("[EXPORT] Exporting to CSV...")
with open(CSV_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "perp_id", "name", "fake_ssn", "fake_address", "threat_level",
        "sighting_id", "timestamp", "location", "screenshot_path"
    ])
    for perp in perps:
        for s in perp.sightings:
            writer.writerow([
                perp.id, perp.name, perp.fake_ssn, perp.fake_address, perp.threat_level,
                s.id, s.timestamp.isoformat(), s.location, s.screenshot_path
            ])

print(f"[EXPORT] CSV exported to {CSV_PATH}")
print("[EXPORT] All done. Stark-style data dump complete ✅")
