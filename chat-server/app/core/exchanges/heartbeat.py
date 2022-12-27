import json

from aio_pika import RobustChannel, Message
from aio_pika.abc import AbstractRobustExchange, ExchangeType, DeliveryMode
from fastapi.encoders import jsonable_encoder

from app.core.config import Settings
from app.core.models.heartbeat import HeartbeatMessage


class HeartbeatExchange:
    def __init__(self, settings: Settings, channel: RobustChannel):
        self.__message_ttl = settings.HEARTBEAT_MESSAGE_TTL
        self.__exchange_name = settings.HEARTBEAT_EXCHANGE_NAME
        self.__exchange: AbstractRobustExchange | None = None
        self.__channel = channel

    async def setup(self):
        self.__exchange = await self.__channel.declare_exchange(
            name=self.__exchange_name,
            type=ExchangeType.FANOUT,
        )

    @staticmethod
    async def create(settings: Settings, channel: RobustChannel):
        exchange = HeartbeatExchange(settings, channel)
        await exchange.setup()
        return exchange

    async def publish(self, heartbeat_message: HeartbeatMessage):
        serialized_message = json.dumps(jsonable_encoder(heartbeat_message)).encode("utf-8")
        await self.__exchange.publish(
            Message(
                body=serialized_message,
                content_type="application/json",
                delivery_mode=DeliveryMode.PERSISTENT,
                expiration=self.__message_ttl
            ),
            routing_key=''
        )
