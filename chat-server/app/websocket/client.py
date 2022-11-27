import starlette.websockets
from starlette.websockets import WebSocket

from app.core.client import ChatClient
from app.core.models.user import User


class WebSocketChatClient(ChatClient):
    def __init__(self, user: User, websocket: WebSocket):
        super().__init__(user)
        self.__websocket = websocket

    async def send_json(self, message):
        try:
            await self.__websocket.send_json(message)
        except starlette.websockets.WebSocketDisconnect as e:
            raise ChatClient.DisconnectException from e
