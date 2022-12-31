from redis.asyncio import Redis, ConnectionPool

from app.core.config import Settings


async def get_connection_pool(settings: Settings):
    pool = ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)
    yield pool
    await pool.disconnect()


def get_connection(pool: ConnectionPool):
    return Redis(connection_pool=pool)
