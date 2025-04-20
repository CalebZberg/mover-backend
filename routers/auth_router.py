# routers/auth_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from repositories.json_repository import JSONRepository

# Define your User model here (or import from models.py)
class User(BaseModel):
    username: str
    password: str

router = APIRouter(prefix="/auth", tags=["auth"])
user_repo = JSONRepository("data/users.json")

@router.post("/login")
def login(user: User):
    users = user_repo.list(User)
    # Stub: succeed if any user in JSON matches username
    if any(u.username == user.username for u in users):
        return {"success": True, "username": user.username}
    raise HTTPException(status_code=401, detail="Invalid credentials")
