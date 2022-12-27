from pydantic import BaseModel


class HeartbeatMessage(BaseModel):
    server_name: str
    advertised_address: str
    num_clients: int
    max_clients: int
