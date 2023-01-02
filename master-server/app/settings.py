from pydantic import BaseSettings, AnyUrl
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    JWT_SECRET: str
    DATABASE_URL: str
    BROKER_URL: str
    HEARTBEAT_EXCHANGE_NAME: str = "heartbeat-exchange"
    HEARTBEAT_RESPONSE_TIME: int = 30
    BACKEND_CORS_ORIGINS: List[AnyUrl] = []

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
