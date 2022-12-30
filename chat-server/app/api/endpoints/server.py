from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.config import Settings, AdvertisingSettings
from app.core.container import Container
from app.core.models.info import ServerInfo
from app.core.services.chat import ChatService

router = APIRouter(prefix="/server")


@router.get("/info")
@inject
async def get_server_info(
        settings: Settings = Depends(Provide[Container.settings]),
        advertising_settings: AdvertisingSettings = Depends(Provide[Container.advertising_settings]),
        chat_service: ChatService = Depends(Provide[Container.chat_service])
):
    return ServerInfo(
        server_name=advertising_settings.SERVER_NAME,
        num_clients=chat_service.get_num_clients(),
        max_clients=settings.MAX_CLIENTS,
    )
