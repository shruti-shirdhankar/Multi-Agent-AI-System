from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite DB
DATABASE_URL = "sqlite:///./shared_memory.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class InputMetadata(Base):
    __tablename__ = "inputs"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    classification = Column(String)
    timestamp = Column(DateTime, default=datetime.now)


class ExtractedField(Base):
    __tablename__ = "extracted"
    id = Column(Integer, primary_key=True, index=True)
    agent = Column(String)
    data = Column(Text)


class Action(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(Text)
    triggered_by = Column(String)
    timestamp = Column(DateTime, default=datetime.now)


class Trace(Base):
    __tablename__ = "traces"
    id = Column(Integer, primary_key=True, index=True)
    trace_data = Column(Text)


# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)
