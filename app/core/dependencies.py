from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.service import TradingCache
from app.core.database import get_db_session
from app.repositories.trading import TradingRepository


async def get_trading_repository(
    session: AsyncSession = Depends(get_db_session),
) -> TradingRepository:
    """DI-провайдер репозитория торговых данных."""

    return TradingRepository(session=session)


def get_trading_cache(request: Request) -> TradingCache:
    """DI-провайдер кэша торговых данных (Redis)."""

    return request.app.state.trading_cache
