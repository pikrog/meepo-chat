from abc import ABC, abstractmethod


class DisconnectException(Exception):
    def __init__(self):
        super().__init__("client disconnected")


class AbstractChatClient(ABC):
    @abstractmethod
    async def close(self):
        raise NotImplementedError

    @abstractmethod
    async def send_json(self, message):
        raise NotImplementedError

    @abstractmethod
    async def receive_json(self):
        raise NotImplementedError
