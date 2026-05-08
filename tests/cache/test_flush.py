from __future__ import annotations

import pytest

from app.cache.flush import TRADING_KEY_PATTERN, flush_trading_keys


@pytest.mark.asyncio
async def test_flush_trading_keys_removes_trading_prefix(fake_redis) -> None:
    await fake_redis.set("trading:dates:last_days:1", "[]")
    await fake_redis.set("other:key", "1")

    deleted = await flush_trading_keys(fake_redis)

    assert deleted == 1
    assert await fake_redis.get("trading:dates:last_days:1") is None
    assert await fake_redis.get("other:key") == "1"


def test_trading_key_pattern() -> None:
    assert TRADING_KEY_PATTERN == "trading:*"
