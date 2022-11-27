from typing import List, Union

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "chat-server"
    BACKEND_CORS_ORIGINS: List[AnyUrl] = []

    MASTER_SERVER_URL: AnyHttpUrl
    JWT_SECRET: str

    SERVER_NAME: str

    REDIS_URL: AnyUrl
    REDIS_CHAT_STREAM: str = "chat-events"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"


# @lru_cache()
# def get_settings():
#     return Settings()
