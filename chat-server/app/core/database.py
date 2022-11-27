import logging

from redis.asyncio import Redis, ConnectionPool
from redis.exceptions import ConnectionError

from app.core.config import Settings


async def get_connection_pool(settings: Settings):
    pool = ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)
    yield pool
    await pool.disconnect()


def get_connection(pool: ConnectionPool):
    return Redis(connection_pool=pool)


async def test_database_connection(connection: Redis, logger=logging.getLogger(__name__)):
    logger.info("Testing database connection...")
    try:
        await connection.ping()
    except ConnectionError as exc:
        logger.exception("Connection failed", exc_info=exc)
        raise
