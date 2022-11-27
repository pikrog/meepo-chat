import starlette
from fastapi.encoders import jsonable_encoder
from starlette.websockets import WebSocket

from app.core.models.message import MessageIn, Message, MessageType
from app.core.models.user import User
from app.core.models.socket import SocketOpcode, SocketMessage
from app.core.services.chat import ChatService
from app.websocket.client import WebSocketChatClient


class ClientHandler:
    def __init__(self, service: ChatService, websocket: WebSocket, user: User):
        self.__service = service
        self.__websocket = websocket
        self.__user = user
        self.__client = WebSocketChatClient(user, websocket)

    async def _send_json(self, message: SocketMessage):
        await self.__websocket.send_json(jsonable_encoder(message))

    async def _execute_single_operation(self, message: SocketMessage):
        if message.opcode == SocketOpcode.quit:
            return True
        elif message.opcode == SocketOpcode.heartbeat:
            response = SocketMessage(opcode=SocketOpcode.heartbeat, data="ok")
            await self._send_json(response)
        elif message.opcode == SocketOpcode.user_list:
            user_list = await self.__service.get_user_list()
            response = SocketMessage(opcode=SocketOpcode.user_list, data=user_list)
            await self._send_json(response)
        elif message.opcode == SocketOpcode.chat:
            message_in = MessageIn(**message.data)
            chat_message = Message(
                type=MessageType.chat,
                sender=self.__user.name,
                text=message_in.text
            )
            await self.__service.send_message(chat_message)
        return False

    async def _execute_operations(self):
        final_operation = False
        while not final_operation:
            try:
                payload = await self.__websocket.receive_json()
                message = SocketMessage(**payload)
                final_operation = await self._execute_single_operation(message)
            except ValueError as e:
                response = SocketMessage(opcode=SocketOpcode.error, data=str(e))
                await self._send_json(response)
        await self.__websocket.close()

    async def handle(self):
        await self.__websocket.accept()

        try:
            await self.__service.join(self.__client)
            await self._execute_operations()
        except starlette.websockets.WebSocketDisconnect:
            pass
        finally:
            await self.__service.leave(self.__client)
