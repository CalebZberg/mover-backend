from pydantic import BaseModel

class QuoteRequest(BaseModel):
    origin: str
    destination: str
    date: str
    inventory: str

class QuoteResponse(QuoteRequest):
    distance: str
    estimate: float
