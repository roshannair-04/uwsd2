import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# === DB setup with absolute path ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'uwsd.db')}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

print(f"[DB INIT] Using database at: {DATABASE_URL}")


# === Models ===
class Perpetrator(Base):
    __tablename__ = "perpetrators"

    id = Base.metadata.tables.get("id")
    id = __import__("sqlalchemy").Column(__import__("sqlalchemy").Integer, primary_key=True)
    name = __import__("sqlalchemy").Column(__import__("sqlalchemy").String, nullable=False)
    fake_ssn = __import__("sqlalchemy").Column(__import__("sqlalchemy").String, unique=True)
    fake_address = __import__("sqlalchemy").Column(__import__("sqlalchemy").String)
    threat_level = __import__("sqlalchemy").Column(__import__("sqlalchemy").Integer)


class Sighting(Base):
    __tablename__ = "sightings"

    id = __import__("sqlalchemy").Column(__import__("sqlalchemy").Integer, primary_key=True)
    perp_id = __import__("sqlalchemy").Column(__import__("sqlalchemy").Integer, __import__("sqlalchemy").ForeignKey("perpetrators.id"))
    timestamp = __import__("sqlalchemy").Column(__import__("sqlalchemy").DateTime)
    location = __import__("sqlalchemy").Column(__import__("sqlalchemy").String)
    screenshot_path = __import__("sqlalchemy").Column(__import__("sqlalchemy").String)


def init_db():
    print("[DB INIT] Creating tables if not exist...")
    Base.metadata.create_all(engine)
    print("[DB INIT] Tables ready.")
