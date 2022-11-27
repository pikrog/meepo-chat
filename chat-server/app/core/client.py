from asyncio import Lock

from fastapi.encoders import jsonable_encoder

from app.core.models.user import User


class ChatClient:
    class DisconnectException(Exception):
        def __init__(self):
            super().__init__("client disconnected")

    def __init__(self, user: User):
        self.user = user

    async def send_json(self, message):
        raise NotImplementedError


class ChatClientGroup:
    def __init__(self):
        self.__clients: set[ChatClient] = set()
        self.__clients_lock = Lock()

    async def add_client(self, client: ChatClient):
        async with self.__clients_lock:
            self.__clients.add(client)

    async def remove_client(self, client: ChatClient):
        async with self.__clients_lock:
            if client not in self.__clients:
                return
            self.__clients.remove(client)

    async def get_user_list(self):
        async with self.__clients_lock:
            return [client.user for client in self.__clients]

    async def is_user_in_list(self, user: User):
        async with self.__clients_lock:
            return next((client for client in self.__clients if client.user.name == user.name), None) is not None

    async def send_message(self, message):
        await self._broadcast(message)

    async def _broadcast(self, message):
        dead_clients = []
        serializable_message = jsonable_encoder(message, exclude_unset=True)
        async with self.__clients_lock:
            clients = self.__clients.copy()
        for client in clients:
            try:
                await client.send_json(serializable_message)
            except ChatClient.DisconnectException:
                dead_clients.append(client)
        for dead_client in dead_clients:
            await self.remove_client(dead_client)
