from app.database.session import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, nullable = False)
    name = Column(String, nullable = True)
    phone = Column(String, nullable = True)
    avatar_url = Column(String, nullable = True)
    password = Column(String, nullable = False)
    created_at = Column(DateTime(timezone = True), server_default=func.now())