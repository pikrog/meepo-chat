from enum import Enum
from typing import Any

from pydantic import BaseModel


class SocketOpcode(str, Enum):
    heartbeat = "heartbeat"
    user_list = "user_list"
    quit = "quit"
    chat = "chat"
    error = "error"


class SocketMessage(BaseModel):
    opcode: SocketOpcode
    data: Any
