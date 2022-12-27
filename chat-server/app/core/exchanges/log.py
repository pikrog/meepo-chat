import json

from aio_pika import RobustChannel, ExchangeType, Message
from aio_pika.abc import AbstractRobustExchange, AbstractRobustQueue, DeliveryMode
from fastapi.encoders import jsonable_encoder

from app.core.config import Settings
from app.core.models.chat import ChatMessage


class LogExchange:
    def __init__(self, settings: Settings, channel: RobustChannel):
        self.__exchange_name = settings.LOG_EXCHANGE_NAME
        self.__exchange: AbstractRobustExchange | None = None
        self.__queue_name = settings.LOG_QUEUE_NAME
        self.__queue: AbstractRobustQueue | None = None
        self.__channel = channel

    async def setup(self):
        self.__exchange = await self.__channel.declare_exchange(
            name=self.__exchange_name,
            type=ExchangeType.DIRECT,
        )
        self.__queue = await self.__channel.declare_queue(
            name=self.__queue_name,
            durable=True,
        )
        await self.__queue.bind(
            exchange=self.__exchange,
            routing_key=self.__queue_name,
        )

    @staticmethod
    async def create(settings: Settings, channel: RobustChannel):
        queue = LogExchange(settings, channel)
        await queue.setup()
        return queue

    async def publish(self, chat_message: ChatMessage):
        serialized_message = json.dumps(jsonable_encoder(chat_message, exclude_none=True)).encode("utf-8")
        # todo: publisher acks & queue overflow
        await self.__exchange.publish(
            Message(
                body=serialized_message,
                content_type="application/json",
                delivery_mode=DeliveryMode.PERSISTENT,
            ),
            routing_key=self.__queue_name
        )
