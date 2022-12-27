import asyncio

from app.core.exchanges.log import LogExchange
from app.core.models.chat import ChatMessage, ChatMessageType
from app.core.models.socket import SocketMessage
from app.core.models.user import User
from app.core.repositories.chat import ChatRepository
from app.core.server.client import ChatClient
from app.core.server.group import ChatClientGroup


class ChatService:
    def __init__(self, repository: ChatRepository, group: ChatClientGroup, log_exchange: LogExchange):
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

    async def join(self, client: ChatClient):
        self.__group.add_client(client)
        await self._send_join_message(client.user)

    async def leave(self, client: ChatClient):
        user_was_in_list = self.__group.remove_client(client)
        if user_was_in_list:
            await self._send_leave_message(client.user)
