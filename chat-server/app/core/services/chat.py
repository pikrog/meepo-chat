from app.core.client import ChatClientGroup, ChatClient
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

    async def get_user_list(self):
        return await self.__group.get_user_list()

    async def is_user_in_list(self, user: User):
        return await self.__group.is_user_in_list(user)

    async def join(self, client: ChatClient):
        await self.__group.add_client(client)
        await self._send_join_message(client.user)

    async def leave(self, client: ChatClient):
        await self.__group.remove_client(client)
        await self._send_leave_message(client.user)
