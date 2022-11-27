from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis

from app.core.config import Settings
from app.core.models.message import Message


class ChatRepository:
    def __init__(self, settings: Settings, redis: Redis):
        self.__messages_stream = settings.REDIS_CHAT_STREAM
        self.__redis = redis

    async def append_message(self, message: Message):
        await self.__redis.xadd(
            name=self.__messages_stream,
            fields=jsonable_encoder(message, exclude_unset=True, exclude={"id"})
        )

    async def get_messages(self):
        messages = await self.__redis.xrange(self.__messages_stream)
        return [Message(**m[1], id=m[0]) for m in messages]
