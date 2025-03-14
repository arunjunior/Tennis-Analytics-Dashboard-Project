import requests
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# API setup
API_KEY = "api_key"
BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json"
url = f"{BASE_URL}?api_key={API_KEY}"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

# Debug response
print(f"Status Code: {response.status_code}")
print(f"Raw Response: {response.text[:200]}...")  # Truncated for readability
if response.status_code != 200:
    print("API call failed!")
    exit()

data = response.json()

# MySQL setup
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_HOST = "localhost"
MYSQL_DB = "tennis_analytics_db"
engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")

Base = declarative_base()


class Competitor(Base):
    __tablename__ = "Competitors"
    competitor_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    country_code = Column(String(3), nullable=False)
    abbreviation = Column(String(10), nullable=False)


class CompetitorRanking(Base):
    __tablename__ = "Competitor_Rankings"
    rank_id = Column(Integer, primary_key=True, autoincrement=True)
    rank = Column(Integer, nullable=False)
    movement = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    competitions_played = Column(Integer, nullable=False)
    competitor_id = Column(String(50), ForeignKey("Competitors.competitor_id"))


Base.metadata.create_all(engine)

# Store data
with Session(engine) as session:
    ranking_groups = data.get("rankings", [])


    for group in ranking_groups:
        competitor_rankings = group.get("competitor_rankings", [])

        for ranking in competitor_rankings:
            competitor_data = ranking.get("competitor", {})
            if competitor_data:
                session.merge(Competitor(
                    competitor_id=competitor_data["id"],
                    name=competitor_data["name"],
                    country=competitor_data.get("country", "Unknown"),
                    country_code=competitor_data.get("country_code", "UNK"),
                    abbreviation=competitor_data.get("abbreviation", "UNK")
                ))

            session.merge(CompetitorRanking(
                rank=ranking["rank"],
                movement=ranking["movement"],
                points=ranking["points"],
                competitions_played=ranking["competitions_played"],
                competitor_id=competitor_data["id"]
            ))

    session.commit()
    print("Data inserted into database!")

# Verify a sample data from database
with Session(engine) as session:
    sample_competitors = session.query(Competitor).limit(3).all()
    print("Sample Competitors:")
    for c in sample_competitors:
        print(f"ID: {c.competitor_id}, Name: {c.name}, Country: {c.country}")
    sample_rankings = session.query(CompetitorRanking).limit(3).all()
    print("Sample Rankings:")
    for r in sample_rankings:
        print(f"Rank ID: {r.rank_id}, Rank: {r.rank}, Points: {r.points}, Competitor ID: {r.competitor_id}")
