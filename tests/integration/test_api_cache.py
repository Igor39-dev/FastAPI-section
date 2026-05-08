from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_trading_results_second_request_uses_redis_cache(
    async_client: AsyncClient,
    mock_trading_repository,
) -> None:
    r1 = await async_client.get("/api/v1/trading/results/", params={"limit": 10})
    r2 = await async_client.get("/api/v1/trading/results/", params={"limit": 10})
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert mock_trading_repository.get_trading_results.await_count == 1
