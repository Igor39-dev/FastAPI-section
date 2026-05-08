from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import date
from typing import Any
from unittest.mock import AsyncMock

import fakeredis
import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from app.core.dependencies import get_trading_repository
from app.main import app
from app.models.trading_results import SpimexTradingResult
from app.repositories.trading import TradingRepository


@pytest.fixture
def fake_redis() -> fakeredis.FakeAsyncRedis:
    return fakeredis.FakeAsyncRedis(decode_responses=True)


@pytest.fixture(autouse=True)
def _patch_main_redis_and_db_health(monkeypatch: pytest.MonkeyPatch, fake_redis: fakeredis.FakeAsyncRedis) -> None:
    monkeypatch.setattr("app.main.redis_async.from_url", lambda *args, **kwargs: fake_redis)
    monkeypatch.setattr("app.main.check_db_connection", AsyncMock(return_value=True))


def _sample_rows() -> list[SpimexTradingResult]:
    return [
        SpimexTradingResult(
            id=1,
            date=date(2026, 1, 1),
            oil_id="O1",
            delivery_type_id="T1",
            delivery_basis_id="B1",
            volume=10.5,
            total=100.0,
            count=2,
        )
    ]


@pytest.fixture
def mock_trading_repository() -> Any:
    repo = AsyncMock(spec=TradingRepository)
    repo.get_last_trading_dates = AsyncMock(return_value=[date(2026, 1, 2), date(2026, 1, 1)])
    repo.get_trading_dynamics = AsyncMock(return_value=_sample_rows())
    repo.get_trading_results = AsyncMock(return_value=_sample_rows())
    return repo


@pytest.fixture
async def async_client(mock_trading_repository: Any) -> AsyncIterator[AsyncClient]:
    async def _override_repo() -> Any:
        return mock_trading_repository

    app.dependency_overrides[get_trading_repository] = _override_repo
    transport = ASGITransport(app=app)
    async with LifespanManager(app):
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    app.dependency_overrides.clear()
