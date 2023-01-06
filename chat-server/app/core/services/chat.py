import asyncio

from app.core.config import Settings, AdvertisingSettings
from app.core.exchanges.log import LogExchange
from app.core.models.chat import ChatMessage, ChatMessageType, LoggedChatMessage, ChatError
from app.core.models.socket import SocketMessage
from app.core.models.user import User
from app.core.repositories.chat import ChatRepository
from app.core.server.client import AbstractChatClient
from app.core.server.group import ChatClientGroup


class JoinError(ChatError):
    def __init__(self, name, message, *args):
        super().__init__(name, message, *args)


class UserAlreadyInRoomError(JoinError):
    def __init__(self):
        super().__init__("user_already_in_room", "the user is already in the room")


class FullRoomError(JoinError):
    def __init__(self):
        super().__init__("full_room", "the room is full")


class ChatService:
    def __init__(
            self,
            settings: Settings,
            advertising_settings: AdvertisingSettings,
            repository: ChatRepository,
            group: ChatClientGroup,
            log_exchange: LogExchange
    ):
        self.__settings = settings
        self.__advertising_settings = advertising_settings
        self.__repository = repository
        self.__group = group
        self.__log_exchange = log_exchange

    async def _send_join_message(self, joining_user: User):
        message = ChatMessage(
            type=ChatMessageType.join,
            sender=joining_user.name,
            sender_id=joining_user.id
        )
        await self.send_message(message)

    async def _send_leave_message(self, leaving_user: User):
        message = ChatMessage(
            type=ChatMessageType.leave,
            sender=leaving_user.name,
            sender_id=leaving_user.id
        )
        await self.send_message(message)

    async def send_message(self, message: ChatMessage):
        logged_message = LoggedChatMessage.from_chat_message(
            message,
            self.__advertising_settings.ADVERTISED_ADDRESS,
            self.__advertising_settings.ADVERTISED_PORT
        )
        results = await asyncio.gather(
            self.__repository.append_message(message),
            self.__log_exchange.publish(logged_message),
        )
        message.id = results[0]
        socket_message = SocketMessage.from_chat_message(message)
        await self.__group.send_message(socket_message)

    async def get_messages(
            self,
            start_id: str | int | bytes | None = None,
            count: int | None = None
    ):
        return await self.__repository.get_messages(start_id, count)

    def get_user_list(self):
        return list(self.__group.get_user_list_view())

    def is_user_in_list(self, user: User):
        return user in self.__group.get_user_list_view()

    def get_num_clients(self):
        return len(self.__group.get_client_list_view())

    async def join(self, client: AbstractChatClient, user: User):
        if self.is_user_in_list(user):
            raise UserAlreadyInRoomError
        if self.get_num_clients() >= self.__settings.MAX_CLIENTS:
            raise FullRoomError

        self.__group.add_client(client, user)
        await self._send_join_message(user)

    async def leave(self, client: AbstractChatClient):
        user = self.__group.remove_client(client)
        if user is not None:
            await self._send_leave_message(user)
