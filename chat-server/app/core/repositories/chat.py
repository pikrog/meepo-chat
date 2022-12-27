from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis

from app.core.config import Settings
from app.core.models.chat import ChatMessage


class ChatRepository:
    def __init__(self, settings: Settings, redis: Redis):
        self.__messages_stream = settings.REDIS_CHAT_STREAM
        self.__redis = redis

    async def append_message(self, message: ChatMessage):
        await self.__redis.xadd(
            name=self.__messages_stream,
            fields=jsonable_encoder(message, exclude_unset=True, exclude={"id"})
        )

    async def get_messages(self):
        messages = await self.__redis.xrange(self.__messages_stream)
        return [ChatMessage(**m[1], id=m[0]) for m in messages]
