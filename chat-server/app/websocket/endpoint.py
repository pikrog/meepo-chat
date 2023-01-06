from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from starlette.websockets import WebSocket

from app.core.container import Container
from app.core.models.chat import QuitMessage
from app.core.models.socket import SocketMessage
from app.core.security.auth import get_user, CredentialsError, get_token_from_query_param, get_token_from_cookie
from app.core.server.auth import get_token_by_handshake
from app.core.server.client import DisconnectException
from app.core.server.handler import ChatClientHandler
from app.core.services.chat import ChatService
from app.websocket.client import WebSocketChatClient


@inject
async def websocket_endpoint(
    websocket: WebSocket,
    cookie_access_token: str | None = Depends(get_token_from_cookie),
    query_access_token: str | None = Depends(get_token_from_query_param),
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
):
    await websocket.accept()

    chat_client = WebSocketChatClient(websocket)

    try:
        access_token = cookie_access_token or query_access_token or await get_token_by_handshake(chat_client)
        try:
            user = get_user(access_token)
            auth_success_message = SocketMessage.create_auth_success()
            await chat_client.send_json(jsonable_encoder(auth_success_message))
            chat_client_handler = ChatClientHandler(chat_service, chat_client, user)
            await chat_client_handler.handle()
        except CredentialsError as error:
            quit_message = QuitMessage.from_error(error)
            error_message = SocketMessage.from_quit_message(quit_message)
            await chat_client.send_json(jsonable_encoder(error_message))
            await chat_client.close()
    except DisconnectException:
        pass
