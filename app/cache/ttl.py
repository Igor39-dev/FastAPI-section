from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.core.config import CACHE_RESET_HOUR, CACHE_RESET_MINUTE


def seconds_until_cache_reset(*, tz: ZoneInfo, now: datetime | None = None) -> int:
    """Секунды до ближайшего момента сброса кэша (сегодня или завтра в CACHE_RESET_HOUR:MINUTE по tz)."""

    if now is None:
        now = datetime.now(tz=tz)
    else:
        now = now.astimezone(tz)

    target = now.replace(
        hour=CACHE_RESET_HOUR,
        minute=CACHE_RESET_MINUTE,
        second=0,
        microsecond=0,
    )
    if now >= target:
        target += timedelta(days=1)

    delta = int((target - now).total_seconds())
    return max(delta, 1)


def seconds_until_next_scheduled_flush(*, tz: ZoneInfo, now: datetime | None = None) -> float:
    """Секунды (float) до следующего запуска фонового flush в CACHE_RESET_HOUR:MINUTE."""

    if now is None:
        now = datetime.now(tz=tz)
    else:
        now = now.astimezone(tz)

    target = now.replace(
        hour=CACHE_RESET_HOUR,
        minute=CACHE_RESET_MINUTE,
        second=0,
        microsecond=0,
    )
    if now >= target:
        target += timedelta(days=1)

    return max((target - now).total_seconds(), 0.1)
