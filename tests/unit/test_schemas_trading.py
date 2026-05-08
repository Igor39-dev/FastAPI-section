from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.trading import TradingDynamicsQuery, TradingResultsQuery


def test_trading_dynamics_query_rejects_inverted_dates() -> None:
    with pytest.raises(ValidationError):
        TradingDynamicsQuery(
            start_date=date(2026, 2, 10),
            end_date=date(2026, 2, 1),
        )


def test_trading_results_query_limit_bounds() -> None:
    with pytest.raises(ValidationError):
        TradingResultsQuery(limit=0)
    with pytest.raises(ValidationError):
        TradingResultsQuery(limit=1001)
