from app.core.config import Settings
from app.core.exchanges.heartbeat import HeartbeatExchange
from app.core.models.heartbeat import HeartbeatMessage
from app.core.services.chat import ChatService


class HeartbeatService:
    def __init__(self, settings: Settings, chat_service: ChatService, heartbeat_exchange: HeartbeatExchange):
        self.__settings = settings
        self.__chat_service = chat_service
        self.__exchange = heartbeat_exchange

    def get_heartbeat_message(self):
        num_clients = len(self.__chat_service.get_user_list())
        return HeartbeatMessage(
            server_name=self.__settings.SERVER_NAME,
            advertised_address=self.__settings.ADVERTISED_ADDRESS,
            num_clients=num_clients,
            max_clients=self.__settings.MAX_CLIENTS,
        )

    def send_heartbeat(self):
        heartbeat_message = self.get_heartbeat_message()
        self.__exchange.publish(heartbeat_message)
