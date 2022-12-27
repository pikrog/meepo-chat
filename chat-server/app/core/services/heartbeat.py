from app.core.config import Settings
from app.core.exchanges.heartbeat import HeartbeatExchange
from app.core.models.heartbeat import HeartbeatMessage
from app.core.services.chat import ChatService


class HeartbeatService:
    def __init__(self, settings: Settings, chat_service: ChatService, heartbeat_exchange: HeartbeatExchange):
        self.__server_name = settings.SERVER_NAME
        self.__advertised_address = settings.ADVERTISED_ADDRESS
        self.__max_clients = settings.MAX_CLIENTS
        self.__chat_service = chat_service
        self.__exchange = heartbeat_exchange

    def get_heartbeat_message(self):
        num_clients = len(self.__chat_service.get_user_list())
        return HeartbeatMessage(
            server_name=self.__server_name,
            advertised_address=self.__advertised_address,
            num_clients=num_clients,
            max_clients=self.__max_clients,
        )

    def send_heartbeat(self):
        heartbeat_message = self.get_heartbeat_message()
        self.__exchange.publish(heartbeat_message)
