from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional 
from sqlalchemy.ext.declarative import declarative_base


def create_sql_light_engine(path: Optional[str] = None):
    if path is None:
        path = settings.sqlite_database_url
    
    if not path:
        raise ValueError("SQL Lite environment variable is not set")
    
    return create_engine(f"sqlite:///{path}")

engine = create_sql_light_engine()
Session = sessionmaker(engine)
Base = declarative_base()

def get_db():
    if Session is None:
        raise ValueError("Database not configured.")
    
    db = Session()

    try:
        yield db
    finally:
        db.close()