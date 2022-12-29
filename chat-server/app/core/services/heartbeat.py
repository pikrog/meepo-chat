from app.core.config import Settings
from app.core.exchanges.heartbeat import HeartbeatExchange
from app.core.models.heartbeat import HeartbeatMessage
from app.core.services.chat import ChatService


class HeartbeatService:
    def __init__(self, settings: Settings, heartbeat_exchange: HeartbeatExchange):
        self.__settings = settings
        self.__exchange = heartbeat_exchange

    def get_heartbeat_message(self):
        return HeartbeatMessage(
            advertised_address=self.__settings.ADVERTISED_ADDRESS,
            advertised_port=self.__settings.ADVERTISED_PORT,
        )

    async def send_heartbeat(self):
        heartbeat_message = self.get_heartbeat_message()
        await self.__exchange.publish(heartbeat_message)
