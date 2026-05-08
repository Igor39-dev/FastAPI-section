from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from app.cache.ttl import seconds_until_cache_reset, seconds_until_next_scheduled_flush


def test_seconds_until_cache_reset_before_reset_same_day() -> None:
    tz = ZoneInfo("UTC")
    now = datetime(2026, 5, 8, 10, 0, tzinfo=tz)
    seconds = seconds_until_cache_reset(tz=tz, now=now)
    assert seconds == (14 * 3600 + 11 * 60) - (10 * 3600)


def test_seconds_until_cache_reset_after_reset_goes_to_next_day() -> None:
    tz = ZoneInfo("UTC")
    now = datetime(2026, 5, 8, 15, 0, tzinfo=tz)
    seconds = seconds_until_cache_reset(tz=tz, now=now)
    expected = int(
        (datetime(2026, 5, 9, 14, 11, tzinfo=tz) - now).total_seconds()
    )
    assert seconds == expected


def test_seconds_until_next_scheduled_flush_positive() -> None:
    tz = ZoneInfo("UTC")
    now = datetime(2026, 5, 8, 14, 10, tzinfo=tz)
    wait = seconds_until_next_scheduled_flush(tz=tz, now=now)
    assert 50 <= wait <= 70
