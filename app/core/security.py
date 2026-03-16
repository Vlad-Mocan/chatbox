from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends
from jose import JWTError, jwt

import bcrypt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database.session import get_db
from app.exceptions.custom_exceptions import InvalidAuthorizationException, UserNotFoundException
from app.repositories.user_repository import UserRepository

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

security = HTTPBearer(auto_error=False)

def create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": str(user_id), "exp": expire}, settings.secret_key, settings.algorithm)

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security), db: Session = Depends(get_db)):
    if not credentials or credentials.scheme != "Bearer":
        raise InvalidAuthorizationException()
    
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidAuthorizationException()
        user_id = int(user_id)
    except (JWTError, ValueError):
        raise InvalidAuthorizationException()
    
    user = UserRepository(db).get_by_id(user_id)

    if not user:
        raise UserNotFoundException()
    
    return user