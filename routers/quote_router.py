from fastapi import APIRouter
from pydantic import BaseModel
from services.quote import calculate_quote
from services.db import get_conn
from sqlalchemy import text

router = APIRouter(prefix="/quote")

class QuoteRequest(BaseModel):
    origin: str
    destination: str
    date: str
    inventory: str

@router.post("/")
def create_quote(req: QuoteRequest):
    # Calculate quote
    distance_text, estimate = calculate_quote(req.origin, req.destination)

    # Save to DB
    with get_conn().connect() as conn:
        insert_sql = text("""
            INSERT INTO quotes (origin, destination, date, inventory, distance, estimate)
            VALUES (:origin, :destination, :date, :inventory, :distance, :estimate)
        """)
        conn.execute(insert_sql, {
            "origin": req.origin,
            "destination": req.destination,
            "date": req.date,
            "inventory": req.inventory,
            "distance": distance_text,
            "estimate": estimate
        })
        conn.commit()

    # Return to frontend
    return {
        "origin": req.origin,
        "destination": req.destination,
        "date": req.date,
        "inventory": req.inventory,
        "distance": distance_text,
        "estimate": estimate
    }
