from __future__ import annotations

import json
from datetime import date
from unittest.mock import AsyncMock

import pytest

from app.cache.keys import dates_key
from app.cache.service import TradingCache
from app.schemas.trading import TradingDateResponse


@pytest.mark.asyncio
async def test_trading_cache_hit_skips_loader(fake_redis) -> None:
    key = dates_key(7)
    payload = [{"date": "2026-01-01"}]
    await fake_redis.set(key, json.dumps(payload))

    cache = TradingCache(fake_redis, timezone="UTC")
    loader = AsyncMock()

    out = await cache.get_json_list(key, TradingDateResponse, loader)

    assert len(out) == 1
    assert out[0].date.isoformat() == "2026-01-01"
    loader.assert_not_called()


@pytest.mark.asyncio
async def test_trading_cache_miss_calls_loader_and_sets_key(fake_redis) -> None:
    key = dates_key(99)
    cache = TradingCache(fake_redis, timezone="UTC")

    async def loader() -> list[TradingDateResponse]:
        return [TradingDateResponse(date=date(2026, 2, 1))]

    out = await cache.get_json_list(key, TradingDateResponse, loader)

    assert len(out) == 1
    raw = await fake_redis.get(key)
    assert raw is not None
    assert json.loads(raw) == [{"date": "2026-02-01"}]
    ttl = await fake_redis.ttl(key)
    assert ttl > 0
