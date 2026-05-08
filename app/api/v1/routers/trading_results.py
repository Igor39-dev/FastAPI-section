from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_trading_repository
from app.repositories.trading import TradingRepository
from app.schemas.trading import TradingDateResponse

router = APIRouter(prefix="/api/v1/trading", tags=["trading"])


@router.get("/dates/", response_model=list[TradingDateResponse])
async def get_last_trading_dates(
    repository: Annotated[TradingRepository, Depends(get_trading_repository)],
    last_days: int = Query(default=30, ge=1, description="Количество последних торговых дней"),
) -> list[TradingDateResponse]:
    """Возвращает список дат последних торговых дней."""

    dates = await repository.get_last_trading_dates(last_days=last_days)
    return [TradingDateResponse(date=trading_date) for trading_date in dates]
