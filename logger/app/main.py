import logging

import pika

from settings import Settings


def on_message_received(logger, channel, method, _, body):
    # todo: save to db instead of printing
    logger.info(f"Received: {body.decode()}")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("meepo-logger")
    logging.getLogger("pika").setLevel(logging.WARNING)

    settings = Settings()

    logger.info(f"Connecting to {settings.BROKER_URL}")

    connection = pika.BlockingConnection(pika.connection.URLParameters(settings.BROKER_URL))
    channel = connection.channel()

    channel.queue_declare(queue=settings.LOG_QUEUE_NAME, durable=True)

    channel.basic_qos(prefetch_count=settings.QOS_PREFETCH_COUNT)

    channel.basic_consume(
        queue=settings.LOG_QUEUE_NAME,
        on_message_callback=lambda ch, method, deliver, body: on_message_received(logger, ch, method, deliver, body)
    )

    logger.info(f"Consuming messages from {settings.LOG_QUEUE_NAME}")

    channel.start_consuming()


if __name__ == "__main__":
    main()
