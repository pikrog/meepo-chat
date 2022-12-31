from dependency_injector import containers, providers

from app.core import database, broker
from app.core.config import Settings, AdvertisingSettings
from app.core.exchanges.heartbeat import HeartbeatExchange
from app.core.exchanges.log import LogExchange
from app.core.repositories.chat import ChatRepository
from app.core.server.group import ChatClientGroup
from app.core.services.chat import ChatService
from app.core.services.heartbeat import HeartbeatService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        packages=[
            "app"
        ],
    )

    settings = providers.Singleton(
        Settings
    )

    advertising_settings = providers.Singleton(
        AdvertisingSettings.from_basic_settings,
        basic_settings=settings,
    )

    database_pool = providers.Resource(
        database.get_connection_pool,
        settings=settings,
    )

    database_connection = providers.Factory(
        database.get_connection,
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

    broker_connection = providers.Resource(
        broker.get_connection,
        settings=settings
    )

    broker_channel = providers.Singleton(
        broker.get_channel,
        connection=broker_connection
    )

    log_exchange = providers.Singleton(
        LogExchange.create,
        settings=settings,
        channel=broker_channel
    )

    chat_service = providers.Factory(
        ChatService,
        settings=settings,
        advertising_settings=advertising_settings,
        repository=chat_repository,
        group=client_group,
        log_exchange=log_exchange,
    )

    heartbeat_exchange = providers.Singleton(
        HeartbeatExchange.create,
        settings=settings,
        channel=broker_channel,
    )

    heartbeat_service = providers.Factory(
        HeartbeatService,
        advertising_settings=advertising_settings,
        heartbeat_exchange=heartbeat_exchange,
    )
