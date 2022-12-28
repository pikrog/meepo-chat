from fastapi import APIRouter, FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from app.api.endpoints import chat, server
from app.api.endpoints.chat import UserNotInRoomError
from app.core.security.auth import CredentialsError

routers = [
    chat.router,
    server.router,
]


def get_api_router():
    api_router = APIRouter(prefix="/api")
    for router in routers:
        api_router.include_router(router)
    return api_router


def credentials_error_handler(_: Request, exc: CredentialsError):
    return PlainTextResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=str(exc))


def user_not_in_room_handler(_: Request, exc: UserNotInRoomError):
    return PlainTextResponse(status_code=status.HTTP_403_FORBIDDEN, content=str(exc))


def setup_api(app: FastAPI):
    app.include_router(get_api_router())
    app.add_exception_handler(CredentialsError, credentials_error_handler)
    app.add_exception_handler(UserNotInRoomError, user_not_in_room_handler)
