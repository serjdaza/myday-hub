"""App settings, read from environment variables only.

Add new settings here AND to .env.example.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str  # required, e.g. postgresql+psycopg://user:pass@host:5432/db
    static_dir: str = "/app/static"  # where the built React app lives (prod image)
    log_level: str = "info"


@lru_cache
def get_settings() -> Settings:
    return Settings()
