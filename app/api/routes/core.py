from fastapi import APIRouter, Depends
from app.models.user import User

router = APIRouter()

@router.get("/healthz")
def healthz():
    return {"ok": True, "service": "chatbox-api", "version": "0.1.0"}