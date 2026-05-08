from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.cache.keys import dates_key, dynamics_key, hash_params, results_key
from app.cache.service import TradingCache
from app.core.dependencies import get_trading_cache, get_trading_repository
from app.repositories.trading import TradingRepository
from app.schemas.trading import TradingDateResponse, TradingDynamicsQuery, TradingResultResponse, TradingResultsQuery

router = APIRouter(prefix="/api/v1/trading", tags=["trading"])


@router.get("/dates/", response_model=list[TradingDateResponse])
async def get_last_trading_dates(
    repository: Annotated[TradingRepository, Depends(get_trading_repository)],
    cache: Annotated[TradingCache, Depends(get_trading_cache)],
    last_days: int = Query(default=30, ge=1, description="Количество последних торговых дней"),
) -> list[TradingDateResponse]:
    """Возвращает список дат последних торговых дней."""

    cache_key = dates_key(last_days)

    async def load() -> list[TradingDateResponse]:
        dates = await repository.get_last_trading_dates(last_days=last_days)
        return [TradingDateResponse(date=trading_date) for trading_date in dates]

    return await cache.get_json_list(cache_key, TradingDateResponse, load)


@router.get("/dynamics/", response_model=list[TradingResultResponse])
async def get_trading_dynamics(
    repository: Annotated[TradingRepository, Depends(get_trading_repository)],
    cache: Annotated[TradingCache, Depends(get_trading_cache)],
    params: Annotated[TradingDynamicsQuery, Depends()],
) -> list[TradingResultResponse]:
    """Возвращает список торгов за заданный период."""

    cache_key = dynamics_key(hash_params(params.model_dump(mode="json")))

    async def load() -> list[TradingResultResponse]:
        rows = await repository.get_trading_dynamics(
            start_date=params.start_date,
            end_date=params.end_date,
            oil_id=params.oil_id,
            delivery_type_id=params.delivery_type_id,
            delivery_basis_id=params.delivery_basis_id,
        )
        return [TradingResultResponse.model_validate(row) for row in rows]

    return await cache.get_json_list(cache_key, TradingResultResponse, load)


@router.get("/results/", response_model=list[TradingResultResponse])
async def get_trading_results(
    repository: Annotated[TradingRepository, Depends(get_trading_repository)],
    cache: Annotated[TradingCache, Depends(get_trading_cache)],
    params: Annotated[TradingResultsQuery, Depends()],
) -> list[TradingResultResponse]:
    """Возвращает последние торговые результаты с фильтрами."""

    cache_key = results_key(hash_params(params.model_dump(mode="json")))

    async def load() -> list[TradingResultResponse]:
        rows = await repository.get_trading_results(
            oil_id=params.oil_id,
            delivery_type_id=params.delivery_type_id,
            delivery_basis_id=params.delivery_basis_id,
            limit=params.limit,
        )
        return [TradingResultResponse.model_validate(row) for row in rows]

    return await cache.get_json_list(cache_key, TradingResultResponse, load)
