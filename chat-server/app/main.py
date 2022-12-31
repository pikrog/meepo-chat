import asyncio
import logging
from functools import partial

import uvicorn
from dependency_injector import providers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import setup_api
from app.core.beacon import run_beacon
from app.core.container import Container
from app.websocket.endpoint import websocket_endpoint


async def _on_app_startup(container: Container):
    settings = container.settings()
    logger = container.logger()

    logger.info("Preparing advertising settings")
    advertising_settings = await container.advertising_settings()

    logger.info("Testing database connection")
    database_connection = await container.database_connection()
    await database_connection.ping()

    logger.info("Testing broker connection")
    heartbeat_service = await container.heartbeat_service()
    await heartbeat_service.send_heartbeat()

    logger.info(f"The server name is \"{advertising_settings.SERVER_NAME}\"")
    logger.info(f"The server will advertise itself as available at "
                f"\"{advertising_settings.ADVERTISED_ADDRESS}:{advertising_settings.ADVERTISED_PORT}\"")

    logger.info("Initialization complete")

    asyncio.create_task(
        run_beacon(
            logger=logger,
            heartbeat_service=heartbeat_service,
            settings=settings
        )
    )


def get_app(container: Container):
    settings = container.settings()

    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.container = container

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_api(_app)

    _app.add_api_websocket_route("/ws", websocket_endpoint)

    _app.add_event_handler("startup", partial(_on_app_startup, container))

    return _app


def get_production_app():
    container = Container()
    container.logger.override(providers.Singleton(
        logging.getLogger,
        name="gunicorn.error"
    ))
    return get_app(container)


if __name__ == "__main__":
    _container = Container()
    port = _container.settings().SERVER_PORT
    uvicorn.run(partial(get_app, _container), factory=True, port=port)
