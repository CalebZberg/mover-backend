# main.py

from dotenv import load_dotenv
import os

load_dotenv()
MAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth_router import router as auth_router
from routers.quote_router import router as quote_router

app = FastAPI(
    title="Bub's Movers API",
    description="FastAPI service for authentication and quotes",
    version="1.0.0"
)

# === BROAD CORS (for debugging) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(quote_router)

@app.get("/")
def read_root():
    return {"message": "API is running"}
