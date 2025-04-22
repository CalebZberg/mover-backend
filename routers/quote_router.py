# routers/quote_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import insert, select
from database import SessionLocal, quotes
from services.distance_service import calculate_quote

class QuoteRequest(BaseModel):
    origin: str
    destination: str
    date: str | None = None
    inventory: str | None = None

class QuoteResponse(BaseModel):
    distance: str
    estimate: float

router = APIRouter(prefix="/quote", tags=["quote"])

@router.post("/", response_model=QuoteResponse)
def create_quote(req: QuoteRequest):
    distance_text, estimate = calculate_quote(req.origin, req.destination)

    # persist to RDS
    with SessionLocal() as db:
        stmt = insert(quotes).values(
            origin=req.origin,
            destination=req.destination,
            date=req.date,
            inventory=req.inventory,
            distance=distance_text,
            estimate=estimate,
        )
        db.execute(stmt)
        db.commit()

    return QuoteResponse(distance=distance_text, estimate=estimate)

@router.get("/", response_model=list[QuoteResponse])
def list_quotes():
    with SessionLocal() as db:
        stmt = select(quotes.c.distance, quotes.c.estimate)
        rows = db.execute(stmt).all()

    return [QuoteResponse(distance=r.distance, estimate=r.estimate) for r in rows]
