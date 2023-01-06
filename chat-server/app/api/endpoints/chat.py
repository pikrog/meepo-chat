from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.params import Query
from pydantic import PositiveInt

from app.core.container import Container
from app.core.models.chat import ChatMessage, ChatMessageIn, ChatMessageType, ChatMessagesRequest
from app.core.models.user import User
from app.core.security.auth import get_user
from app.core.services.chat import ChatService

router = APIRouter(prefix="/chat")


class UserNotInRoomError(Exception):
    def __init__(self):
        super().__init__("the user is not in the room")


@router.get("/messages")
@inject
async def get_chat_messages(
        request: ChatMessagesRequest,
        chat_service: ChatService = Depends(Provide[Container.chat_service]),
        user: User = Depends(get_user),
):
    if not chat_service.is_user_in_list(user):
        raise UserNotInRoomError

    return await chat_service.get_messages(request.start_id, request.count)


@router.put("/send")
@inject
async def send_chat_message(
        message_in: ChatMessageIn,
        user: User = Depends(get_user),
        chat_service: ChatService = Depends(Provide[Container.chat_service])
):
    if not chat_service.is_user_in_list(user):
        raise UserNotInRoomError

    message = ChatMessage(
        type=ChatMessageType.chat,
        sender=user.name,
        text=message_in.text,
    )
    await chat_service.send_message(message)
