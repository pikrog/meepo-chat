import pika

from settings import Settings


def on_message_received(ch, method, _, body):
    # todo: save to db instead of printing
    print(f"{body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    settings = Settings()

    connection = pika.BlockingConnection(pika.connection.URLParameters(settings.BROKER_URL))
    channel = connection.channel()

    channel.queue_declare(queue=settings.LOG_QUEUE_NAME, durable=True)

    channel.basic_qos(prefetch_count=settings.QOS_PREFETCH_COUNT)
    channel.basic_consume(queue=settings.LOG_QUEUE_NAME, on_message_callback=on_message_received)

    channel.start_consuming()


if __name__ == "__main__":
    main()
