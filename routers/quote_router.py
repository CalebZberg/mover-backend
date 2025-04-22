# routers/quote_router.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.db import get_conn
from services.distance_service import calculate_quote

class QuoteRequest(BaseModel):
    origin: str
    destination: str
    date: str  # or date
    inventory: str

router = APIRouter(prefix="/quote")

@router.post("/", status_code=201)
async def create_quote(req: QuoteRequest, conn=Depends(get_conn)):
    dist_text, estimate = calculate_quote(req.origin, req.destination)

    result = conn.execute(text(
        "INSERT INTO quotes (origin, destination, date, inventory, distance, estimate) "
        "VALUES (:o, :d, :dt, :inv, :dist, :est) "
        "RETURNING id"
    ), {
        "o": req.origin,
        "d": req.destination,
        "dt": req.date,
        "inv": req.inventory,
        "dist": dist_text,
        "est": estimate,
    })
    new_id = result.scalar_one()
    conn.commit()

    return {"id": new_id, "distance": dist_text, "estimate": estimate}
