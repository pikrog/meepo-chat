import aio_pika

from app.core.config import Settings


async def get_connection(settings: Settings):
    connection = await aio_pika.connect_robust(settings.BROKER_URL)
    yield connection
    await connection.close()


async def get_channel(connection: aio_pika.RobustConnection):
    return await connection.channel()
