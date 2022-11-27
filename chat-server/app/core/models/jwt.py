from pydantic import BaseModel


class JwtPayload(BaseModel):
    username: str
