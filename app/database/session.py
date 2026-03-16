from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base

from app.exceptions.custom_exceptions import (
    PostgresEnvironmentNotSetException,
    SqlLiteEnvironmentNotSetException,
)


def create_sql_light_engine(path: Optional[str] = None):
    if path is None:
        path = settings.sqlite_database_url

    if not path:
        raise SqlLiteEnvironmentNotSetException()

    return create_engine(f"sqlite:///{path}")


def create_postgre_engine(connection_string: Optional[str] = None):
    if connection_string is None:
        connection_string = settings.postgres_database_url

    if not connection_string:
        raise PostgresEnvironmentNotSetException()

    return create_engine(connection_string)


engine = create_postgre_engine()
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
