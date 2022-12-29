from pydantic import BaseModel


class ServerInfo(BaseModel):
    server_name: str
    num_clients: int
    max_clients: int
