from functools import lru_cache

from pydantic import BaseSettings, AmqpDsn, AnyUrl


class Settings(BaseSettings):
    DATABASE_URL: AnyUrl
    BROKER_URL: AmqpDsn
    LOG_QUEUE_NAME: str = "log-queue"
    QOS_PREFETCH_COUNT: int = 1

    class Config:
        case_sensitive = True


@lru_cache
def get_settings():
    return Settings()
