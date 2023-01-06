from fastapi.encoders import jsonable_encoder

from app.core.models.chat import ChatMessageIn, ChatMessage, ChatMessageType, ChatMessagesRequest, GenericChatError, \
    QuitMessage
from app.core.models.socket import SocketMessage, SocketOpcode
from app.core.models.user import User
from app.core.server.client import AbstractChatClient
from app.core.services.chat import ChatService, JoinError


class ChatClientHandler:
    def __init__(self, service: ChatService, client: AbstractChatClient, user: User):
        self.__service = service
        self.__client = client
        self.__user = user

    async def _send_json(self, message: SocketMessage):
        await self.__client.send_json(jsonable_encoder(message))

    async def _execute_single_operation(self, message: SocketMessage):
        if message.opcode == SocketOpcode.quit:
            response = SocketMessage.from_quit_message(message.data)
            await self._send_json(response)
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
                sender=self.__user.name,
                sender_id=self.__user.id,
                text=message_in.text
            )
            await self.__service.send_message(chat_message)
        elif message.opcode == SocketOpcode.messages:
            request = ChatMessagesRequest(**message.data)
            messages = await self.__service.get_messages(request.start_id, request.count)
            response = SocketMessage.from_chat_message_list(messages)
            await self._send_json(response)
        return False

    async def _execute_operations(self):
        final_operation = False
        while not final_operation:
            try:
                payload = await self.__client.receive_json()
                message = SocketMessage(**payload)
                final_operation = await self._execute_single_operation(message)
            except ValueError as exc:
                error = GenericChatError(str(exc))
                response = SocketMessage.from_error(error)
                await self._send_json(response)

    async def handle(self):
        try:
            await self.__service.join(self.__client, self.__user)
            await self._execute_operations()
            await self.__client.close()
        except JoinError as error:
            quit_message = QuitMessage.from_error(error)
            response_message = SocketMessage.from_quit_message(quit_message)
            await self._send_json(response_message)
            await self.__client.close()
        finally:
            await self.__service.leave(self.__client)
