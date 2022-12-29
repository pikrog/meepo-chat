from starlette.websockets import WebSocket, WebSocketDisconnect

from app.core.models.user import User
from app.core.server.client import AbstractChatClient, DisconnectException


class WebSocketChatClient(AbstractChatClient):
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
            raise DisconnectException
        try:
            await self.__websocket.send_json(message)
        except WebSocketDisconnect as e:
            self.__is_closed = True
            raise DisconnectException from e

    async def receive_json(self):
        if self.__is_closed:
            raise DisconnectException
        try:
            return await self.__websocket.receive_json()
        except WebSocketDisconnect as e:
            self.__is_closed = True
            raise DisconnectException from e
