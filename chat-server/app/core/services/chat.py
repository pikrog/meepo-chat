import asyncio

from app.core.config import Settings
from app.core.exchanges.log import LogExchange
from app.core.models.chat import ChatMessage, ChatMessageType
from app.core.models.socket import SocketMessage
from app.core.models.user import User
from app.core.repositories.chat import ChatRepository
from app.core.server.client import AbstractChatClient
from app.core.server.group import ChatClientGroup


class JoinError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class AlreadyInRoomError(JoinError):
    def __init__(self):
        super().__init__("the user is already in the room")


class FullRoomError(JoinError):
    def __init__(self):
        super().__init__("the chat room is full")


class ChatService:
    def __init__(
            self,
            settings: Settings,
            repository: ChatRepository,
            group: ChatClientGroup,
            log_exchange: LogExchange
    ):
        self.__settings = settings
        self.__repository = repository
        self.__group = group
        self.__log_exchange = log_exchange

    async def _send_join_message(self, joining_user: User):
        message = ChatMessage(type=ChatMessageType.join, sender=joining_user.name)
        await self.send_message(message)

    async def _send_leave_message(self, leaving_user: User):
        message = ChatMessage(type=ChatMessageType.leave, sender=leaving_user.name)
        await self.send_message(message)

    async def send_message(self, message: ChatMessage):
        await asyncio.gather(
            self.__repository.append_message(message),
            self.__log_exchange.publish(message),
        )
        socket_message = SocketMessage.from_chat_message(message)
        await self.__group.send_message(socket_message)

    async def get_messages(self):
        return await self.__repository.get_messages()

    def get_user_list(self):
        return self.__group.get_user_list()

    def is_user_in_list(self, user: User):
        return self.__group.is_user_in_list(user)

    async def join(self, client: AbstractChatClient):
        if self.__group.is_user_in_list(client.user):
            raise AlreadyInRoomError
        if len(self.__group.get_user_list()) >= self.__settings.MAX_CLIENTS:
            raise FullRoomError

        self.__group.add_client(client)
        await self._send_join_message(client.user)

    async def leave(self, client: AbstractChatClient):
        user_was_in_list = self.__group.remove_client(client)
        if user_was_in_list:
            await self._send_leave_message(client.user)
