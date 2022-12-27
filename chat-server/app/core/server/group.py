from fastapi.encoders import jsonable_encoder

from app.core.server.client import ChatClient
from app.core.models.user import User


class ChatClientGroup:
    def __init__(self):
        self.__clients: set[ChatClient] = set()

    def add_client(self, client: ChatClient):
        self.__clients.add(client)

    def remove_client(self, client: ChatClient):
        if client not in self.__clients:
            return False
        self.__clients.remove(client)
        return True

    def get_user_list(self):
        return [client.user for client in self.__clients]

    def is_user_in_list(self, user: User):
        return next((client for client in self.__clients if client.user.name == user.name), None) is not None

    async def send_message(self, message):
        await self._broadcast(message)

    async def _broadcast(self, message):
        dead_clients = []
        serializable_message = jsonable_encoder(message, exclude_unset=True)
        clients = self.__clients.copy()
        for client in clients:
            try:
                await client.send_json(serializable_message)
            except ChatClient.DisconnectException:
                dead_clients.append(client)
        for dead_client in dead_clients:
            self.remove_client(dead_client)
