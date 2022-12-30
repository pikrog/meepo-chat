import asyncio
import logging
from functools import partial

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import setup_api
from app.core.beacon import run_beacon
from app.core.container import Container
from app.websocket.endpoint import websocket_endpoint


async def _on_app_startup(container: Container, logger: logging.Logger):
    settings = container.settings()

    logger.info("Preparing advertising settings")
    advertising_settings = await container.advertising_settings()

    logger.info("Testing database connection")
    database_connection = await container.database_connection()
    await database_connection.ping()

    logger.info("Testing broker connection")
    heartbeat_service = await container.heartbeat_service()

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


def get_app(container: Container, logger: logging.Logger):
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

    _app.add_event_handler("startup", partial(_on_app_startup, container, logger))

    return _app


def get_production_app():
    container = Container()
    logger = logging.getLogger("gunicorn.error")
    return get_app(container, logger)


if __name__ == "__main__":
    _container = Container()
    _logger = logging.getLogger("uvicorn")
    port = _container.settings().SERVER_PORT
    uvicorn.run(partial(get_app, _container, _logger), factory=True, port=port)
