from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Perpetrator(Base):
    __tablename__ = "perpetrators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    threat_level = Column(Integer, default=1)  # GTA-style stars
    fake_ssn = Column(String, default="000-00-0000")
    fake_address = Column(String, default="Unknown")

    sightings = relationship("Sighting", back_populates="perp")

class Sighting(Base):
    __tablename__ = "sightings"

    id = Column(Integer, primary_key=True, index=True)
    perp_id = Column(Integer, ForeignKey("perpetrators.id"))
    timestamp = Column(DateTime)
    location = Column(String)
    screenshot_path = Column(String)

    perp = relationship("Perpetrator", back_populates="sightings")

