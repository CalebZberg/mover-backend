# services/db.py
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

engine: Engine = create_engine(
    os.getenv("DATABASE_URL"),
    connect_args={"sslmode": "require"},
    future=True,
)

def get_conn():
    return engine.connect()
