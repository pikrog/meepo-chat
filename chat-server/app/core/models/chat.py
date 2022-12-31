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


class LoggedChatMessage(BaseModel):
    id: str | None = None
    type: ChatMessageType
    sender: str | None = None
    sender_id: int | None = None
    timestamp: datetime
    text: str | None = None
    advertised_address: str
    advertised_port: int

    @staticmethod
    def from_chat_message(chat_message: ChatMessage, advertised_address: str, advertised_port: int):
        return LoggedChatMessage(
            id=chat_message.id,
            type=chat_message.type,
            sender=chat_message.sender,
            sender_id=chat_message.sender_id,
            timestamp=chat_message.timestamp,
            text=chat_message.text,
            advertised_address=advertised_address,
            advertised_port=advertised_port,
        )
