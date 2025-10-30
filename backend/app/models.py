
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

DB_URL = os.environ.get("DATABASE_URL", "sqlite:///./pulse.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    region = Column(String, nullable=True)

class Consent(Base):
    __tablename__ = "consents"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    marketing = Column(Boolean, default=False)
    analytics = Column(Boolean, default=False)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String, index=True)
    properties = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

class Sponsor(Base):
    __tablename__ = "sponsors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    industry = Column(String, nullable=True)

class TrendSignal(Base):
    __tablename__ = "trend_signals"
    id = Column(Integer, primary_key=True, index=True)
    segment = Column(String, index=True)
    metric = Column(String, index=True)
    value = Column(Float)
    sample_size = Column(Integer, default=0)
    generated_at = Column(DateTime, default=datetime.utcnow)
