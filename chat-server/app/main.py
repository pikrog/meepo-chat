import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import setup_api
from app.core.container import Container
from app.websocket.endpoint import websocket_endpoint


def get_app():
    container = Container()
    settings = container.settings()

    # database = await container.database_connection()

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

    # _app.add_event_handler("startup", partial(test_database_connection, database, logging.getLogger("uvicorn")))
    # await test_database_connection(database)

    return _app


if __name__ == "__main__":
    uvicorn.run(get_app, factory=True)
