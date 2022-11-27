from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from starlette import status
from starlette.websockets import WebSocket

from app.core.container import Container
from app.core.security.auth import get_user, get_token_from_cookie, CredentialsError
from app.core.services.chat import ChatService
from app.websocket.handler import ClientHandler


@inject
async def websocket_endpoint(
    websocket: WebSocket,
    access_token: str | None = Depends(get_token_from_cookie),
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
):
    try:
        user = get_user(access_token)
    except CredentialsError as exc:
        await websocket.close(code=status.HTTP_403_FORBIDDEN, reason=str(exc))
        return

    if await chat_service.is_user_in_list(user):
        await websocket.close(code=status.HTTP_403_FORBIDDEN, reason="Already in the room")
        return

    await ClientHandler(chat_service, websocket, user).handle()
