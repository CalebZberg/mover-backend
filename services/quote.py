import requests
import os
from dotenv import load_dotenv

load_dotenv()

MAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def calculate_quote(origin: str, destination: str):
    try:
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={MAPS_KEY}"
        response = requests.get(url)
        data = response.json()

        if data["rows"] and data["rows"][0]["elements"]:
            distance_info = data["rows"][0]["elements"][0]
            if distance_info["status"] == "OK":
                distance_text = distance_info["distance"]["text"]
                distance_value = distance_info["distance"]["value"]  # in meters
                estimate = round(50 + (distance_value / 1609.34) * 25, 2)
                return distance_text, estimate
    except:
        pass

    return "n/a", 75.0