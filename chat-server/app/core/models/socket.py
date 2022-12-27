from enum import Enum
from typing import Any

from pydantic import BaseModel

from app.core.models.chat import ChatMessage
from app.core.models.user import User


class SocketOpcode(str, Enum):
    heartbeat = "heartbeat"
    user_list = "user_list"
    quit = "quit"
    chat = "chat"
    error = "error"


class SocketMessage(BaseModel):
    opcode: SocketOpcode
    data: Any

    @staticmethod
    def from_chat_message(message: ChatMessage):
        return SocketMessage(opcode=SocketOpcode.chat, data=message)

    @staticmethod
    def from_error(error: str):
        return SocketMessage(opcode=SocketOpcode.error, data=error)

    @staticmethod
    def from_user_list(user_list: list[User]):
        return SocketMessage(opcode=SocketOpcode.error, data=user_list)

    @staticmethod
    def create_heartbeat(message: str = "ok"):
        return SocketMessage(opcode=SocketOpcode.heartbeat, data=message)

    @staticmethod
    def create_quit(message: str = "unknown reason"):
        return SocketMessage(opcode=SocketOpcode.quit, data=message)
