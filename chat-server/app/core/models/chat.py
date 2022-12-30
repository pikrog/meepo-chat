from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from typing import Any


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
    sender_id: int | None = None
    timestamp: datetime
    text: str | None = None

    def __init__(self, **data: Any):
        if "timestamp" not in data:
            data["timestamp"] = datetime.utcnow()
        super().__init__(**data)
