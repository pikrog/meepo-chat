from app.core.config import AdvertisingSettings
from app.core.exchanges.heartbeat import HeartbeatExchange
from app.core.models.heartbeat import HeartbeatMessage


class HeartbeatService:
    def __init__(self, advertising_settings: AdvertisingSettings, heartbeat_exchange: HeartbeatExchange):
        self.__advertising_settings = advertising_settings
        self.__exchange = heartbeat_exchange

    def get_heartbeat_message(self):
        return HeartbeatMessage(
            advertised_address=self.__advertising_settings.ADVERTISED_ADDRESS,
            advertised_port=self.__advertising_settings.ADVERTISED_PORT,
        )

    async def send_heartbeat(self):
        heartbeat_message = self.get_heartbeat_message()
        await self.__exchange.publish(heartbeat_message)
