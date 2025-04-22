# routers/quote_router.py

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
    dist_text, estimate = calculate_quote(req.origin, req.destination)

    conn = get_conn()
    conn.execute(text("""
        INSERT INTO quotes (origin, destination, date, inventory, distance, estimate)
        VALUES (:origin, :destination, :date, :inventory, :distance, :estimate)
    """), {
        "origin": req.origin,
        "destination": req.destination,
        "date": req.date,
        "inventory": req.inventory,
        "distance": dist_text,
        "estimate": estimate
    })

    return {
        "origin": req.origin,
        "destination": req.destination,
        "date": req.date,
        "inventory": req.inventory,
        "distance": dist_text,
        "estimate": estimate
    }
