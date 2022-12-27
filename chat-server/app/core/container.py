from dependency_injector import containers, providers

from app.core.server.group import ChatClientGroup
from app.core.config import Settings
from app.core.database import get_connection_pool, get_connection
from app.core.repositories.chat import ChatRepository
from app.core.services.chat import ChatService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        packages=[
            "app"
        ],
    )

    settings = providers.Singleton(
        Settings
    )

    database_pool = providers.Resource(
        get_connection_pool,
        settings=settings,
    )

    database_connection = providers.Factory(
        get_connection,
        pool=database_pool
    )

    chat_repository = providers.Factory(
        ChatRepository,
        settings=settings,
        redis=database_connection,
    )

    client_group = providers.Singleton(
        ChatClientGroup
    )

    chat_service = providers.Factory(
        ChatService,
        repository=chat_repository,
        group=client_group
    )
