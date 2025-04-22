# database.py
from sqlalchemy import (
    create_engine, MetaData,
    Table, Column,
    Integer, String, Date, Float
)
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Table metadata
metadata = MetaData()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
)

quotes = Table(
    "quotes", metadata,
    Column("id", Integer, primary_key=True),
    Column("origin", String, nullable=False),
    Column("destination", String, nullable=False),
    Column("date", Date),
    Column("inventory", String),
    Column("distance", String, nullable=False),
    Column("estimate", Float, nullable=False),
)

# Create tables if they don't exist yet
metadata.create_all(engine)
