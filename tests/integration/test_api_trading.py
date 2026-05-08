from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_last_trading_dates(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/trading/dates/", params={"last_days": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["date"] == "2026-01-02"


@pytest.mark.asyncio
async def test_get_trading_dynamics(async_client: AsyncClient) -> None:
    response = await async_client.get(
        "/api/v1/trading/dynamics/",
        params={
            "start_date": "2026-01-01",
            "end_date": "2026-01-31",
            "oil_id": "O1",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["oil_id"] == "O1"


@pytest.mark.asyncio
async def test_get_trading_results(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/trading/results/", params={"limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


@pytest.mark.asyncio
async def test_get_trading_dynamics_validation_error(async_client: AsyncClient) -> None:
    response = await async_client.get(
        "/api/v1/trading/dynamics/",
        params={"start_date": "2026-02-10", "end_date": "2026-02-01"},
    )
    assert response.status_code == 422
