# quote_router.py

from fastapi import APIRouter
from models import QuoteRequest, QuoteResponse
from services.maps import calculate_quote
from services.db import get_conn
from sqlalchemy import text

router = APIRouter(prefix="/quote")

@router.post("/", response_model=QuoteResponse)
def create_quote(req: QuoteRequest):
    dist_text, estimate = calculate_quote(req.origin, req.destination)

    conn = get_conn()
    with conn.begin():
        conn.execute(
            text("""
                INSERT INTO quotes (origin, destination, date, inventory, distance, estimate)
                VALUES (:origin, :destination, :date, :inventory, :distance, :estimate)
            """),
            {
                "origin": req.origin,
                "destination": req.destination,
                "date": req.date,
                "inventory": req.inventory,
                "distance": dist_text,
                "estimate": estimate,
            },
        )

    return QuoteResponse(
        origin=req.origin,
        destination=req.destination,
        date=req.date,
        inventory=req.inventory,
        distance=dist_text,
        estimate=estimate
    )