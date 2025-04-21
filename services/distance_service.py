# services/distance_service.py

import os
import httpx
from dotenv import load_dotenv

load_dotenv()  # reads GOOGLE_MAPS_API_KEY from .env

MAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
RATE_PER_MILE = float(os.getenv("RATE_PER_MILE", "5"))  # you can set this in .env too

def calculate_quote(origin: str, destination: str) -> tuple[str, float]:
    """
    Calls Google Distance Matrix API and returns (distance_text, estimate).
    """
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "key": MAPS_KEY,
        "units": "imperial"
    }

    resp = httpx.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    # Basic error handling
    if data.get("status") != "OK":
        raise RuntimeError(f"Google API error: {data.get('status')}")

    element = data["rows"][0]["elements"][0]
    if element.get("status") != "OK":
        raise RuntimeError(f"Route not found: {element.get('status')}")

    distance_text = element["distance"]["text"]         # e.g. "12.3 mi"
    distance_meters = element["distance"]["value"]      # e.g. 19760

    # Convert meters → miles and compute estimate
    miles = distance_meters / 1609.34
    estimate = round(miles * RATE_PER_MILE, 2)

    return distance_text, estimate
