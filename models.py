from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Config
import datetime

Base = declarative_base()

class ExchangeRate(Base):
    __tablename__ = 'exchange_rates'
    id = Column(Integer, primary_key=True)
    currency_from = Column(String, nullable=False)
    currency_to = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Create the database engine
engine = create_engine(f"mssql+pyodbc://{Config.SQL_SERVER['UID']}:{Config.SQL_SERVER['PWD']}@{Config.SQL_SERVER['SERVER']}/{Config.SQL_SERVER['DATABASE']}?driver={Config.SQL_SERVER['DRIVER']}")

# Create the session
Session = sessionmaker(bind=engine)

def setup_db(app):
    Base.metadata.create_all(engine)  # Create all tables if they don't exist
    app.session = Session()  # Attach the session to the app
