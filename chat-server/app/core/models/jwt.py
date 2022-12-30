from pydantic import BaseModel


class JwtPayload(BaseModel):
    user_id: int
    user_name: str
