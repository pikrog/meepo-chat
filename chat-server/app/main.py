import asyncio
import logging
from functools import partial

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import setup_api
from app.core.beacon import run_beacon
from app.core.container import Container
from app.core.database import test_database_connection
from app.websocket.endpoint import websocket_endpoint


async def _on_app_startup(container: Container, logger=logging.getLogger("uvicorn")):
    logger.info("Testing database connection")
    database = await container.database_connection()
    await test_database_connection(database)

    logger.info("Testing broker connection")
    heartbeat_service = await container.heartbeat_service()

    settings = container.settings()
    await settings.auto_config(logger)

    logger.info("Initialization complete")

    asyncio.create_task(
        run_beacon(
            logger=logger,
            heartbeat_service=heartbeat_service,
            settings=settings)
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


def get_default_app():
    return get_app(Container())


if __name__ == "__main__":
    _container = Container()
    port = _container.settings().SERVER_PORT
    uvicorn.run(partial(get_app, _container), factory=True, port=port)
