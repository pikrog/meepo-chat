from typing import List, Union

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, validator, AmqpDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "chat-server"
    BACKEND_CORS_ORIGINS: List[AnyUrl] = []

    JWT_SECRET: str

    SERVER_NAME: str
    MAX_CLIENTS: int = 100
    ADVERTISED_ADDRESS: str

    REDIS_URL: AnyUrl
    REDIS_CHAT_STREAM: str = "chat-events"

    BROKER_URL: AmqpDsn
    LOG_EXCHANGE_NAME: str = "log-exchange"
    LOG_QUEUE_NAME: str = "log-queue"
    HEARTBEAT_EXCHANGE_NAME: str = "heartbeat-exchange"
    HEARTBEAT_MESSAGE_TTL: int = 10

    # noinspection PyMethodParameters
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
