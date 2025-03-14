import requests
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# API setup
API_KEY = "api_key"
BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json"
url = f"{BASE_URL}?api_key={API_KEY}"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Raw Response: {response.text[:200]}...")
data = response.json()

# MySQL setup
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_HOST = "localhost"
MYSQL_DB = "tennis_analytics_db"
engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")

Base = declarative_base()

class Complex(Base):
    __tablename__ = "Complexes"
    complex_id = Column(String(50), primary_key=True)
    complex_name = Column(String(100), nullable=False)

class Venue(Base):
    __tablename__ = "Venues"
    venue_id = Column(String(50), primary_key=True)
    venue_name = Column(String(100), nullable=False)
    city_name = Column(String(100), nullable=False)
    country_name = Column(String(100), nullable=False)
    country_code = Column(String(3), nullable=False)
    timezone = Column(String(100), nullable=False)
    complex_id = Column(String(50), ForeignKey("Complexes.complex_id"))

Base.metadata.create_all(engine)

# Store data
with Session(engine) as session:
    complexes = data.get("complexes", [])
    print(f"Total complexes fetched: {len(complexes)}")

    for comp in complexes:
        session.merge(Complex(
            complex_id=comp["id"],
            complex_name=comp["name"]
        ))

        venues = comp.get("venues", [])
        for venue in venues:
            session.merge(Venue(
                venue_id=venue["id"],
                venue_name=venue["name"],
                city_name=venue.get("city_name", "Unknown"),
                country_name=venue.get("country_name", "Unknown"),
                country_code=venue.get("country_code", "UNK"),
                timezone=venue.get("timezone", "Unknown"),
                complex_id=comp["id"]
            ))

    session.commit()
    print("Data inserted into database!")

# Verify a sample data from database
with Session(engine) as session:
    sample_complexes = session.query(Complex).limit(3).all()
    print("Sample Complexes:")
    for c in sample_complexes:
        print(f"ID: {c.complex_id}, Name: {c.complex_name}")

    sample_venues = session.query(Venue).limit(3).all()
    print("Sample Venues:")
    for v in sample_venues:
        print(f"ID: {v.venue_id}, Name: {v.venue_name}, City: {v.city_name}, Country: {v.country_name}")
