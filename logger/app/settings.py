from pydantic import BaseSettings, AmqpDsn


class Settings(BaseSettings):
    BROKER_URL: AmqpDsn
    LOG_QUEUE_NAME: str = "log-queue"
    QOS_PREFETCH_COUNT: int = 1

    class Config:
        case_sensitive = True
