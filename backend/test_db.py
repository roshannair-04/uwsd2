from database import SessionLocal, init_db, Perpetrator, Sighting

init_db()
session = SessionLocal()

# Add a fake perp
perp = Perpetrator(
    name="John Doe",
    fake_ssn="123-45-6789",
    fake_address="221B Baker Street",
    threat_level=3
)
session.add(perp)
session.commit()

# Query
for p in session.query(Perpetrator).all():
    print(f"{p.name} | SSN: {p.fake_ssn} | Threat: {p.threat_level} stars")
