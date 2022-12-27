import starlette.websockets
from starlette.websockets import WebSocket

from app.core.server.client import ChatClient
from app.core.models.user import User


class WebSocketChatClient(ChatClient):
    def __init__(self, user: User, websocket: WebSocket):
        super().__init__(user)
        self.__websocket = websocket
        self.__is_closed = False

    async def close(self):
        if not self.__is_closed:
            await self.__websocket.close()
            self.__is_closed = True

    async def send_json(self, message):
        if self.__is_closed:
            raise ChatClient.DisconnectException
        try:
            await self.__websocket.send_json(message)
        except starlette.websockets.WebSocketDisconnect as e:
            self.__is_closed = True
            raise ChatClient.DisconnectException from e

    async def receive_json(self):
        if self.__is_closed:
            raise ChatClient.DisconnectException
        try:
            return await self.__websocket.receive_json()
        except starlette.websockets.WebSocketDisconnect as e:
            self.__is_closed = True
            raise ChatClient.DisconnectException from e
