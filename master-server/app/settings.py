from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    JWT_SECRET: str
    DATABASE_URL: str
    BROKER_URL:str
    HEARTBEAT_EXCHANGE_NAME: str = "heartbeat-exchange"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()