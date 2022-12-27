from app.core.server.client import ChatClient
from app.core.server.group import ChatClientGroup
from app.core.models.message import Message, MessageType
from app.core.models.socket import SocketMessage, SocketOpcode
from app.core.models.user import User
from app.core.repositories.chat import ChatRepository


class ChatService:
    def __init__(self, repository: ChatRepository, group: ChatClientGroup):
        self.__repository = repository
        self.__group = group

    async def _send_join_message(self, joining_user: User):
        message = Message(type=MessageType.join, sender=joining_user.name)
        await self.send_message(message)

    async def _send_leave_message(self, leaving_user: User):
        message = Message(type=MessageType.leave, sender=leaving_user.name)
        await self.send_message(message)

    async def send_message(self, message: Message):
        await self.__repository.append_message(message)
        socket_message = SocketMessage(opcode=SocketOpcode.chat, data=message)
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
