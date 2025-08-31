# backend/view_db.py
import os
from sqlalchemy.orm import Session
from backend.database import SessionLocal, init_db, Perpetrator, Sighting

def list_perpetrators(session: Session):
    perps = session.query(Perpetrator).all()
    if not perps:
        print("\n[PERPETRATORS] None found.")
        return
    print("\n=== PERPETRATORS ===")
    for p in perps:
        print(f"ID={p.id} | Name={p.name} | SSN={p.fake_ssn} | "
              f"Address={p.fake_address} | Threat={p.threat_level}★ | "
              f"Sightings={len(p.sightings)}")

def list_sightings(session: Session):
    sightings = session.query(Sighting).all()
    if not sightings:
        print("\n[SIGHTINGS] None found.")
        return
    print("\n=== SIGHTINGS ===")
    for s in sightings:
        print(f"ID={s.id} | PerpID={s.perp_id} | Time={s.timestamp} | "
              f"Location={s.location} | Img={s.screenshot_path}")

def run():
    print("[DB VIEW] Initializing DB...")
    init_db()
    session = SessionLocal()

    list_perpetrators(session)
    list_sightings(session)

    session.close()
    print("\n[DB VIEW] Done.")

if __name__ == "__main__":
    run()
