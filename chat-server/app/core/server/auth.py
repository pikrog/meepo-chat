from fastapi.encoders import jsonable_encoder

from app.core.models.chat import GenericChatError
from app.core.models.socket import SocketMessage, SocketOpcode
from app.core.server.client import AbstractChatClient


async def get_token_by_handshake(client: AbstractChatClient) -> str:
    request_message = SocketMessage.create_auth_request()
    await client.send_json(jsonable_encoder(request_message))
    while True:
        try:
            payload = await client.receive_json()
            message = SocketMessage(**payload)
            if message.opcode == SocketOpcode.auth:
                return message.data
            else:
                error = GenericChatError("not authenticated")
                error_message = SocketMessage.from_error(error)
                await client.send_json(jsonable_encoder(error_message))
        except ValueError as exc:
            error = GenericChatError(str(exc))
            response = SocketMessage.from_error(error)
            await client.send_json(jsonable_encoder(response))
