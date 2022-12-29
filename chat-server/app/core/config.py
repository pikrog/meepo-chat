import logging
from typing import List, Union

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, validator, AmqpDsn

from app.core.ip import get_external_ip_info


class Settings(BaseSettings):
    PROJECT_NAME: str = "chat-server"
    BACKEND_CORS_ORIGINS: List[AnyUrl] = []

    JWT_SECRET: str

    IP_API: AnyHttpUrl
    SERVER_NAME: str | None = None
    SERVER_PORT: int = 8000
    ADVERTISED_ADDRESS: str | None = None
    ADVERTISED_PORT: int | None = None
    MAX_CLIENTS: int = 100

    REDIS_URL: AnyUrl
    REDIS_CHAT_STREAM: str = "chat-events"

    BROKER_URL: AmqpDsn
    LOG_EXCHANGE_NAME: str = "log-exchange"
    LOG_QUEUE_NAME: str = "log-queue"
    HEARTBEAT_EXCHANGE_NAME: str = "heartbeat-exchange"
    HEARTBEAT_INTERVAL: int = 10
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

    async def auto_config(self, logger: logging.Logger):
        if self.ADVERTISED_PORT is None:
            self.ADVERTISED_PORT = self.SERVER_PORT
        if self.ADVERTISED_ADDRESS is None or self.SERVER_NAME is None:
            logger.info("Acquiring external IP info")
            ip, country, city = await get_external_ip_info(self.IP_API)
            logger.info(f"The server is located in {city}, {country}. The external IP is {ip}")
            if self.SERVER_NAME is None:
                self.SERVER_NAME = f"{city}, {country}"
            if self.ADVERTISED_ADDRESS is None:
                self.ADVERTISED_ADDRESS = f"{ip}"
        logger.info(f"The server name is \"{self.SERVER_NAME}\"")
        logger.info(f"The server will advertise itself as available at "
                    f"\"{self.ADVERTISED_ADDRESS}:{self.ADVERTISED_PORT}\"")
