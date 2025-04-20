# routers/quote_router.py

from fastapi import APIRouter
from pydantic import BaseModel
from repositories.json_repository import JSONRepository
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
quote_repo = JSONRepository("data/quotes.json")

@router.post("/", response_model=QuoteResponse)
def create_quote(req: QuoteRequest):
    estimate = calculate_quote(req.origin, req.destination)
    # Persist a record of this quote
    quote_repo.add(QuoteResponse(distance="n/a", estimate=estimate))
    return QuoteResponse(distance="n/a", estimate=estimate)
