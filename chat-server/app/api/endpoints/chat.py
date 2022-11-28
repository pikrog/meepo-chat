from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.container import Container
from app.core.models.message import Message, MessageIn, MessageType
from app.core.models.user import User
from app.core.security.auth import get_user
from app.core.services.chat import ChatService

router = APIRouter(prefix="/chat")


@router.get("/messages", dependencies=[Depends(get_user)])
@inject
async def get_chat_messages(
    chat_service: ChatService = Depends(Provide[Container.chat_service])
):
    return await chat_service.get_messages()


@router.put("/send")
@inject
async def send_chat_message(
        message_in: MessageIn,
        user: User = Depends(get_user),
        chat_service: ChatService = Depends(Provide[Container.chat_service])
):
    if not chat_service.is_user_in_list(user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not in the chat room")
    message = Message(
        type=MessageType.chat,
        sender=user.name,
        text=message_in.text,
    )
    await chat_service.send_message(message)
