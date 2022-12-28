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


async def on_app_startup(container: Container, logger=logging.getLogger("uvicorn")):
    logger.info("Testing database connection")
    database = await container.database_connection()
    await test_database_connection(database)

    logger.info("Testing broker connection")
    heartbeat_service = await container.heartbeat_service()
    await heartbeat_service.send_heartbeat()

    logger.info("Initialization complete")

    settings = container.settings()
    asyncio.create_task(
        run_beacon(
            logger=logger,
            heartbeat_service=heartbeat_service,
            settings=settings)
    )


def get_app():
    container = Container()

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

    _app.add_event_handler("startup", partial(on_app_startup, container))

    return _app


if __name__ == "__main__":
    uvicorn.run(get_app, factory=True)
