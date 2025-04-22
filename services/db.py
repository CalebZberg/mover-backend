import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

engine: Engine = create_engine(
    os.getenv("DATABASE_URL"),
    connect_args={"sslmode": "require"},
    pool_pre_ping=True
)

def get_conn():
    return engine.connect()

def save_quote(origin, destination, date, inventory, distance, estimate):
    with get_conn() as conn:
        conn.execute(text("""
            INSERT INTO quotes (origin, destination, date, inventory, distance, estimate)
            VALUES (:origin, :destination, :date, :inventory, :distance, :estimate)
        """), {
            "origin": origin,
            "destination": destination,
            "date": date,
            "inventory": inventory,
            "distance": distance,
            "estimate": estimate
        })
