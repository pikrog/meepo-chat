from fastapi.encoders import jsonable_encoder

from app.core.server.client import ChatClient, DisconnectException
from app.core.models.message import MessageIn, Message, MessageType
from app.core.models.socket import SocketMessage, SocketOpcode
from app.core.services.chat import ChatService


class ChatClientHandler:
    def __init__(self, service: ChatService, client: ChatClient):
        self.__service = service
        self.__client = client

    async def _send_json(self, message: SocketMessage):
        await self.__client.send_json(jsonable_encoder(message))

    async def _execute_single_operation(self, message: SocketMessage):
        if message.opcode == SocketOpcode.quit:
            return True
        elif message.opcode == SocketOpcode.heartbeat:
            response = SocketMessage(opcode=SocketOpcode.heartbeat, data="ok")
            await self._send_json(response)
        elif message.opcode == SocketOpcode.user_list:
            user_list = self.__service.get_user_list()
            response = SocketMessage(opcode=SocketOpcode.user_list, data=user_list)
            await self._send_json(response)
        elif message.opcode == SocketOpcode.chat:
            message_in = MessageIn(**message.data)
            chat_message = Message(
                type=MessageType.chat,
                sender=self.__client.user.name,
                text=message_in.text
            )
            await self.__service.send_message(chat_message)
        return False

    async def _execute_operations(self):
        final_operation = False
        while not final_operation:
            try:
                payload = await self.__client.receive_json()
                message = SocketMessage(**payload)
                final_operation = await self._execute_single_operation(message)
            except ValueError as e:
                response = SocketMessage(opcode=SocketOpcode.error, data=str(e))
                await self._send_json(response)

    async def handle(self):
        try:
            if self.__service.is_user_in_list(self.__client.user):
                error_message = SocketMessage(opcode=SocketOpcode.error, data="Already in the room")
                await self._send_json(error_message)
                await self.__client.close()
                return

            await self.__service.join(self.__client)
            await self._execute_operations()
            await self.__client.close()
        except DisconnectException:
            pass
        finally:
            await self.__service.leave(self.__client)
