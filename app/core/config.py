from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlite_database_url: Optional[str] = None
    postgres_database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    voyage_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
