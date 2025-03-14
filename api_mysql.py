#COLLECT THE COMPETITION DATA FROM THE API ENDPOINTS AND STORING IN DATABASE

import requests
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# API setup
API_KEY = "api_key"
BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json"
url = f"{BASE_URL}?api_key={API_KEY}"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)
data = response.json()

# MySQL setup
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_HOST = "localhost"
MYSQL_DB = "tennis_analytics_db"
engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")

Base = declarative_base()

# Define Categories table
class Category(Base):
    __tablename__ = "Categories"
    category_id = Column(String(50), primary_key=True)
    category_name = Column(String(100), nullable=False)

# Define Competitions table
class Competition(Base):
    __tablename__ = "Competitions"
    competition_id = Column(String(50), primary_key=True)
    competition_name = Column(String(100), nullable=False)
    parent_id = Column(String(50), nullable=True)
    type = Column(String(20), nullable=False)
    gender = Column(String(10), nullable=False)
    category_id = Column(String(50), ForeignKey("Categories.category_id"))

# Create tables
Base.metadata.create_all(engine)

# Store data
with Session(engine) as session:
    competitions = data.get("competitions", [])
    print(f"Total competitions fetched: {len(competitions)}")

    for comp in competitions:
        # Store category
        category_data = comp.get("category", {})
        if category_data:
            category_id = category_data.get("id")
            if category_id:
                session.merge(Category(
                    category_id=category_id,
                    category_name=category_data.get("name", "Unknown")
                ))

        # Store competition
        session.merge(Competition(
            competition_id=comp["id"],
            competition_name=comp["name"],
            parent_id=comp.get("parent_id"),
            type=comp.get("type", "unknown"),
            gender=comp.get("gender", "unknown"),
            category_id=category_data.get("id")
        ))

    session.commit()
    print("Data inserted into database!")

# Verify a sample data from database
with Session(engine) as session:
    sample = session.query(Competition).limit(5).all()
    for comp in sample:
        print(f"ID: {comp.competition_id}, Name: {comp.competition_name}, Type: {comp.type}, Gender: {comp.gender}")
