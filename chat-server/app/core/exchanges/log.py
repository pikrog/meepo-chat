import json

from aio_pika import RobustChannel, ExchangeType, Message
from aio_pika.abc import AbstractRobustExchange, AbstractRobustQueue, DeliveryMode
from fastapi.encoders import jsonable_encoder

from app.core.config import Settings
from app.core.models.chat import ChatMessage


class LogExchange:
    def __init__(
            self,
            exchange: AbstractRobustExchange,
            queue: AbstractRobustQueue
    ):
        self.__exchange = exchange
        self.__queue = queue

    @staticmethod
    async def create(settings: Settings, channel: RobustChannel):
        exchange = await channel.declare_exchange(
            name=settings.LOG_EXCHANGE_NAME,
            type=ExchangeType.DIRECT,
        )
        queue = await channel.declare_queue(
            name=settings.LOG_QUEUE_NAME,
            durable=True,
        )
        await queue.bind(
            exchange=exchange,
            routing_key=queue.name,
        )
        return LogExchange(exchange, queue)

    async def publish(self, chat_message: ChatMessage):
        serialized_message = json.dumps(jsonable_encoder(chat_message, exclude_none=True)).encode("utf-8")
        # todo: publisher acks & queue overflow
        await self.__exchange.publish(
            Message(
                body=serialized_message,
                content_type="application/json",
                delivery_mode=DeliveryMode.PERSISTENT,
            ),
            routing_key=self.__queue.name
        )
