from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.session import Base, engine
from app.models import user

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=== APPLICATION STARTING ===")
    Base.metadata.create_all(bind=engine)
    print("=== DATABASE READY ===")
    
    yield

    print("=== CLOSING DB CONNECTIONS ===")
    engine.dispose()