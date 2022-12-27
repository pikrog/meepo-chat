from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.services.heartbeat import HeartbeatService

router = APIRouter(prefix="/server")


@router.get("/heartbeat")
@inject
async def get_chat_messages(
    heartbeat_service: HeartbeatService = Depends(Provide[Container.heartbeat_service])
):
    return heartbeat_service.get_heartbeat_message()
