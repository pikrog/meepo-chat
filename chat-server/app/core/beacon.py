import asyncio
import logging

from dependency_injector.wiring import inject

from app.core.config import Settings
from app.core.services.heartbeat import HeartbeatService


@inject
async def run_beacon(
        logger: logging.Logger,
        heartbeat_service: HeartbeatService,
        settings: Settings
):
    logger.info("Sending heartbeats")
    while True:
        try:
            await heartbeat_service.send_heartbeat()
        except Exception as e:
            logger.error("An exception occurred while trying to send a heartbeat")
            logger.exception(e)
        await asyncio.sleep(settings.HEARTBEAT_INTERVAL)
