from __future__ import annotations

import logging

from redis.asyncio import Redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

TRADING_KEY_PATTERN = "trading:*"


async def flush_trading_keys(redis: Redis) -> int:
    """Удаляет все ключи с префиксом trading: (совместимо с несколькими сервисами на одном Redis)."""

    deleted = 0
    try:
        async for key in redis.scan_iter(match=TRADING_KEY_PATTERN):
            await redis.delete(key)
            deleted += 1
    except RedisError as exc:
        logger.warning("redis недоступен, flush пропущен: %s", exc)
        return 0
    logger.info("cache flush completed keys_deleted=%s", deleted)
    return deleted
