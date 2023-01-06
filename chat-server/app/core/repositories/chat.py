from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis

from app.core.config import Settings
from app.core.models.chat import ChatMessage


class ChatRepository:
    def __init__(self, settings: Settings, redis: Redis):
        self.__messages_stream = settings.REDIS_CHAT_STREAM
        self.__redis = redis

    async def append_message(self, message: ChatMessage):
        return await self.__redis.xadd(
            name=self.__messages_stream,
            fields=jsonable_encoder(message, exclude_unset=True, exclude={"id"})
        )

    async def get_messages(
            self,
            start_id: str | int | bytes | None = None,
            count: int | None = None
    ):
        if start_id is None:
            start_id = "+"
        messages = await self.__redis.xrevrange(self.__messages_stream, max=start_id, count=count)
        return [ChatMessage(**m[1], id=m[0]) for m in messages]
