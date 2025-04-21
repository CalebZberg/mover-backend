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
    # 1) Call Google + compute estimate
    distance_text, estimate = calculate_quote(req.origin, req.destination)

    # 2) Persist the quote (saving both fields)
    quote = QuoteResponse(distance=distance_text, estimate=estimate)
    quote_repo.add(quote)

    # 3) Return the real, google-backed quote
    return quote
