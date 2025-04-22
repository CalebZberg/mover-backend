from fastapi import APIRouter
from models import QuoteRequest
from services.maps import calculate_quote
from services.db import get_conn

router = APIRouter(prefix="/quote")

@router.post("/")
def create_quote(req: QuoteRequest):
    dist_text, estimate = calculate_quote(req.origin, req.destination)

    conn = get_conn()  # Already a connection!
    with conn.begin():  # Begin a transaction
        conn.execute(
            "INSERT INTO quotes (origin, destination, date, inventory, distance, estimate) VALUES (%s, %s, %s, %s, %s, %s)",
            (req.origin, req.destination, req.date, req.inventory, dist_text, estimate),
        )

    return {
        "origin": req.origin,
        "destination": req.destination,
        "date": req.date,
        "inventory": req.inventory,
        "distance": dist_text,
        "estimate": estimate,
    }
