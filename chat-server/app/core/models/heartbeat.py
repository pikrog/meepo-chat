from pydantic import BaseModel


class HeartbeatMessage(BaseModel):
    advertised_address: str
    advertised_port: int
