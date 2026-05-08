from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repositories.trading import TradingRepository


async def get_trading_repository(
    session: AsyncSession = Depends(get_db_session),
) -> TradingRepository:
    """DI-провайдер репозитория торговых данных."""

    return TradingRepository(session=session)
