from fastapi import APIRouter, Depends
from app.schemas.user import TokenResponse, UserCreate, UserLogIn, UserResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.user_service import UserService

router = APIRouter()

@router.post("/signup", response_model=TokenResponse, status_code=201)
def signup(body: UserCreate, db: Session = Depends(get_db)):
    return UserService(db).create_user(body)

@router.post("/login", response_model=TokenResponse, status_code=200)
def login(body: UserLogIn, db: Session = Depends(get_db)):
    return UserService(db).login_user(body)