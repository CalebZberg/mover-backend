# services/distance_service.py

def calculate_quote(origin: str, destination: str) -> float:
    """
    Stubbed distance‑based quote calculator.
    In a real app you'd call Google Distance Matrix here,
    parse the distance (e.g. “123 km”), then multiply by a rate.
    For now, we’ll simulate a distance and cost.
    """
    # Simulate distance in km based on string lengths (just for demo!)
    dist_km = abs(len(destination) - len(origin)) * 10 + 50
    rate_per_km = 1.5  # $1.50 per km
    return round(dist_km * rate_per_km, 2)
