from __future__ import annotations

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.repositories.trading import TradingRepository


@pytest.mark.asyncio
async def test_get_last_trading_dates_calls_execute() -> None:
    session = AsyncMock()
    fake_result = MagicMock()
    fake_result.scalars.return_value.all.return_value = [date(2026, 1, 1)]
    session.execute = AsyncMock(return_value=fake_result)

    repo = TradingRepository(session)
    out = await repo.get_last_trading_dates(last_days=5)

    assert out == [date(2026, 1, 1)]
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_trading_results_calls_execute() -> None:
    session = AsyncMock()
    fake_result = MagicMock()
    fake_result.scalars.return_value.all.return_value = []
    session.execute = AsyncMock(return_value=fake_result)

    repo = TradingRepository(session)
    await repo.get_trading_results(oil_id="X", limit=10)

    session.execute.assert_awaited_once()
