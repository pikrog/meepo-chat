from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.websockets import WebSocket

from app.core.models.socket import SocketMessage, SocketOpcode
from app.core.server.handler import ChatClientHandler
from app.core.container import Container
from app.core.security.auth import get_user, get_token_from_cookie, CredentialsError
from app.core.services.chat import ChatService
from app.websocket.client import WebSocketChatClient


@inject
async def websocket_endpoint(
    websocket: WebSocket,
    access_token: str | None = Depends(get_token_from_cookie),
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
):
    await websocket.accept()

    try:
        user = get_user(access_token)
    except CredentialsError as exc:
        error_message = SocketMessage(opcode=SocketOpcode.error, data=str(exc))
        await websocket.send_json(jsonable_encoder(error_message))
        await websocket.close()
        return

    chat_client = WebSocketChatClient(user, websocket)
    chat_client_handler = ChatClientHandler(chat_service, chat_client)
    await chat_client_handler.handle()
