# routers/auth_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from database import SessionLocal, users

class LoginRequest(BaseModel):
    username: str
    password: str

router = APIRouter()

@router.post("/auth/login")
def login(req: LoginRequest):
    with SessionLocal() as db:
        stmt = select(users.c.password).where(users.c.username == req.username)
        stored = db.execute(stmt).scalar_one_or_none()

    if not stored or stored != req.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"success": True, "username": req.username}
