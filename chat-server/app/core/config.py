from typing import List, Union

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, validator, AmqpDsn, BaseModel

from app.core.ip import get_external_ip_info


class Settings(BaseSettings):
    PROJECT_NAME: str = "chat-server"
    BACKEND_CORS_ORIGINS: List[AnyUrl] = []

    JWT_SECRET: str
    JWT_ISSUER: str = "master-server"

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


class AdvertisingSettings(BaseModel):
    SERVER_NAME: str
    ADVERTISED_ADDRESS: str
    ADVERTISED_PORT: int

    @staticmethod
    async def from_basic_settings(basic_settings: Settings):
        advertised_port = basic_settings.ADVERTISED_PORT
        if advertised_port is None:
            advertised_port = basic_settings.SERVER_PORT

        advertised_address = basic_settings.ADVERTISED_ADDRESS
        server_name = basic_settings.SERVER_NAME
        if advertised_address is None or server_name is None:
            ip, country, city = await get_external_ip_info(basic_settings.IP_API)
            if server_name is None:
                server_name = f"{city}, {country}"
            if advertised_address is None:
                advertised_address = f"{ip}"

        return AdvertisingSettings(
            SERVER_NAME=server_name,
            ADVERTISED_ADDRESS=advertised_address,
            ADVERTISED_PORT=advertised_port,
        )
