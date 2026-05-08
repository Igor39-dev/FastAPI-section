from __future__ import annotations

import asyncio
import logging
from zoneinfo import ZoneInfo

from redis.asyncio import Redis

from app.cache.flush import flush_trading_keys
from app.cache.ttl import seconds_until_next_scheduled_flush
from app.core.config import CACHE_RESET_HOUR, CACHE_RESET_MINUTE

logger = logging.getLogger(__name__)


async def cache_flush_scheduler(redis: Redis, timezone: str, stop: asyncio.Event) -> None:
    """Фоновая задача: в CACHE_RESET_HOUR:MINUTE выполняет полный сброс ключей trading:*."""

    tz = ZoneInfo(timezone)
    while not stop.is_set():
        wait_s = seconds_until_next_scheduled_flush(tz=tz)
        try:
            await asyncio.wait_for(stop.wait(), timeout=wait_s)
            break
        except TimeoutError:
            pass
        if stop.is_set():
            break
        logger.info(
            "scheduled cache flush at %02d:%02d (%s)",
            CACHE_RESET_HOUR,
            CACHE_RESET_MINUTE,
            timezone,
        )
        try:
            await flush_trading_keys(redis)
        except Exception:
            logger.exception("scheduled cache flush failed")
