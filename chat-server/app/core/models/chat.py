from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ChatMessageType(str, Enum):
    chat = "chat"
    join = "join"
    leave = "leave"


class ChatMessageIn(BaseModel):
    text: str


class ChatMessage(BaseModel):
    id: str | None = None
    type: ChatMessageType
    sender: str | None = None
    timestamp: datetime = datetime.utcnow()
    text: str | None = None
