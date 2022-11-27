from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class MessageType(str, Enum):
    chat = "chat"
    join = "join"
    leave = "leave"


class MessageIn(BaseModel):
    text: str


class Message(BaseModel):
    id: str | None = None
    type: MessageType
    sender: str | None = None
    timestamp: datetime = datetime.utcnow()
    text: str | None = None
