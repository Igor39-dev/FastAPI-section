from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_ok(async_client: AsyncClient) -> None:
    response = await async_client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["services"]["database"] == "ok"
    assert payload["services"]["redis"] == "ok"


@pytest.mark.asyncio
async def test_health_redis_down_marks_degraded(async_client: AsyncClient) -> None:
    from app.main import app

    redis_client = app.state.redis

    async def _broken_ping() -> None:
        raise ConnectionError("redis down")

    original_ping = redis_client.ping
    redis_client.ping = _broken_ping
    try:
        response = await async_client.get("/health")
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "degraded"
        assert payload["services"]["redis"] == "down"
    finally:
        redis_client.ping = original_ping
