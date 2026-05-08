from __future__ import annotations

import json
import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

from pydantic import BaseModel
from redis.asyncio import Redis
from redis.exceptions import RedisError
from zoneinfo import ZoneInfo

from app.cache.ttl import seconds_until_cache_reset

logger = logging.getLogger(__name__)

TModel = TypeVar("TModel", bound=BaseModel)


class TradingCache:
    """Единая точка входа: чтение/запись JSON в Redis с TTL до момента сброса (14:11)."""

    def __init__(self, redis: Redis, *, timezone: str) -> None:
        self._redis = redis
        self._tz = ZoneInfo(timezone)

    def ttl_seconds(self) -> int:
        return seconds_until_cache_reset(tz=self._tz)

    async def get_json_list(
        self,
        key: str,
        item_type: type[TModel],
        loader: Callable[[], Awaitable[list[TModel]]],
    ) -> list[TModel]:
        try:
            raw = await self._redis.get(key)
        except RedisError as exc:
            logger.warning("redis недоступен, кэш пропущен (get) key=%s: %s", key, exc)
            return await loader()

        if raw is not None:
            logger.info("cache hit key=%s", key)
            parsed: list[object] = json.loads(raw)
            return [item_type.model_validate(item) for item in parsed]

        logger.info("cache miss key=%s", key)
        items = await loader()
        payload = json.dumps([item.model_dump(mode="json") for item in items])
        try:
            await self._redis.set(key, payload, ex=self.ttl_seconds())
        except RedisError as exc:
            logger.warning("redis недоступен, запись в кэш пропущена key=%s: %s", key, exc)
        return items
