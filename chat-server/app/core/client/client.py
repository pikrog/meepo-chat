from app.core.models.user import User


class ChatClient:
    class DisconnectException(Exception):
        def __init__(self):
            super().__init__("client disconnected")

    def __init__(self, user: User):
        self.user = user

    async def close(self):
        raise NotImplementedError

    async def send_json(self, message):
        raise NotImplementedError

    async def receive_json(self):
        raise NotImplementedError
