from fastapi.encoders import jsonable_encoder

from app.core.server.client import AbstractChatClient, DisconnectException
from app.core.models.user import User


class ChatClientGroup:
    def __init__(self):
        self.__clients: dict[AbstractChatClient, User] = dict()

    def add_client(self, client: AbstractChatClient, user: User):
        self.__clients[client] = user

    def remove_client(self, client: AbstractChatClient) -> User | None:
        try:
            user = self.__clients[client]
            self.__clients.pop(client)
            return user
        except KeyError:
            return None

    def get_client_list_view(self):
        return self.__clients.keys()

    def get_user_list_view(self):
        return self.__clients.values()

    async def send_message(self, message):
        await self._broadcast(message)

    async def _broadcast(self, message):
        serializable_message = jsonable_encoder(message, exclude_none=True)
        clients = self.__clients.copy()
        for client in clients.keys():
            try:
                await client.send_json(serializable_message)
            except DisconnectException:
                pass
