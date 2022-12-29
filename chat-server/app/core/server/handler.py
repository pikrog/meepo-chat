from fastapi.encoders import jsonable_encoder

from app.core.server.client import AbstractChatClient, DisconnectException
from app.core.models.chat import ChatMessageIn, ChatMessage, ChatMessageType
from app.core.models.socket import SocketMessage, SocketOpcode
from app.core.services.chat import ChatService, JoinError


class ChatClientHandler:
    def __init__(self, service: ChatService, client: AbstractChatClient):
        self.__service = service
        self.__client = client

    async def _send_json(self, message: SocketMessage):
        await self.__client.send_json(jsonable_encoder(message))

    async def _execute_single_operation(self, message: SocketMessage):
        if message.opcode == SocketOpcode.quit:
            return True
        elif message.opcode == SocketOpcode.heartbeat:
            response = SocketMessage.create_heartbeat()
            await self._send_json(response)
        elif message.opcode == SocketOpcode.user_list:
            user_list = self.__service.get_user_list()
            response = SocketMessage.from_user_list(user_list)
            await self._send_json(response)
        elif message.opcode == SocketOpcode.chat:
            message_in = ChatMessageIn(**message.data)
            chat_message = ChatMessage(
                type=ChatMessageType.chat,
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
                response = SocketMessage.from_error(str(e))
                await self._send_json(response)

    async def handle(self):
        try:
            await self.__service.join(self.__client)
        except JoinError as e:
            error_message = SocketMessage.from_error(str(e))
            try:
                await self._send_json(error_message)
                await self.__client.close()
            except DisconnectException:
                pass
            return

        try:
            await self._execute_operations()
            await self.__client.close()
        except DisconnectException:
            pass
        finally:
            await self.__service.leave(self.__client)
