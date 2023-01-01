import datetime
import json
import logging

import pika
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Message, MessageType, QueuedMessage, InvalidMessage
from settings import Settings


def on_message_received(logger: logging.Logger, database: Session, channel, method, _, body):
    decoded_body = body.decode()
    try:
        deserialized_message = json.loads(decoded_body)
        received_message = QueuedMessage(**deserialized_message)
        message_to_save = Message(
            sender_id=received_message.sender_id,
            advertised_server=f"{received_message.advertised_address}:{received_message.advertised_port}",
            type=MessageType(received_message.type),
            text=received_message.text,
            timestamp=datetime.datetime.fromisoformat(received_message.timestamp)
        )
        database.add(message_to_save)
        database.commit()

        text = f"text=\"{message_to_save.text}\", " if message_to_save.text is not None else ""
        logger.info(f"Saved: {{"
                    f"advertised_server=\"{message_to_save.advertised_server}\", "
                    f"sender_id={message_to_save.sender_id}, type={message_to_save.type}, "
                    f"{text} timestamp={message_to_save.timestamp}"
                    f"}}")
    except (ValueError, TypeError, IntegrityError) as exc:
        logger.warning(f"Invalid message: {decoded_body}")
        logger.exception(exc)
        invalid_message = InvalidMessage(content=decoded_body)
        database.rollback()
        database.add(invalid_message)
        database.commit()
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("meepo-logger")
    logging.getLogger("pika").setLevel(logging.WARNING)

    settings = Settings()

    logger.info(f"Connecting to {settings.BROKER_URL}")

    broker = pika.BlockingConnection(pika.connection.URLParameters(settings.BROKER_URL))
    channel = broker.channel()

    channel.queue_declare(queue=settings.LOG_QUEUE_NAME, durable=True)

    channel.basic_qos(prefetch_count=settings.QOS_PREFETCH_COUNT)

    database = SessionLocal()

    try:
        channel.basic_consume(
            queue=settings.LOG_QUEUE_NAME,
            on_message_callback=lambda ch, method, deliver, body:
                on_message_received(logger, database, ch, method, deliver, body)
        )

        logger.info(f"Consuming messages from {settings.LOG_QUEUE_NAME}")

        channel.start_consuming()
    finally:
        database.close()
        broker.close()


if __name__ == "__main__":
    main()
