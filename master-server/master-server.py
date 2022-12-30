import pika
import jwt
import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from .settings import get_settings


def main():
    settings = get_settings()
    connection = pika.BlockingConnection(pika.connection.URLParameters(settings.BROKER_URL))
    channel = connection.channel()

    channel.queue_declare()

    def receive (ch, method, properties, body):
        print(" [x] Received %r" % body)
    
    channel.basic_consume(on_message_callback=receive, auto_ack=True)
    channel.start_consuming()

    



if __name__ == "__main__":
    main()