# routers/quote_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.quote import calculate_quote
from services.db import get_conn

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
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO quotes (origin, destination, date, inventory, distance, estimate)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (req.origin, req.destination, req.date, req.inventory, dist_text, estimate)
    )
    conn.commit()
    new_id = cur.fetchone()[0]
    cur.close()
    conn.close()

    return {"id": new_id, "distance": dist_text, "estimate": estimate}