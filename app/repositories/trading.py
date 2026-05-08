from datetime import date

from sqlalchemy import Select, desc, distinct, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trading_results import SpimexTradingResult


class TradingRepository:
    """Репозиторий для чтения торговых данных Spimex."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_last_trading_dates(self, last_days: int = 30) -> list[date]:
        stmt = (
            select(distinct(SpimexTradingResult.date))
            .order_by(desc(SpimexTradingResult.date))
            .limit(last_days)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_trading_dynamics(
        self,
        start_date: date,
        end_date: date,
        oil_id: str | None = None,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
    ) -> list[SpimexTradingResult]:
        stmt: Select[tuple[SpimexTradingResult]] = select(SpimexTradingResult).where(
            SpimexTradingResult.date >= start_date,
            SpimexTradingResult.date <= end_date,
        )
        stmt = self._apply_filters(
            stmt=stmt,
            oil_id=oil_id,
            delivery_type_id=delivery_type_id,
            delivery_basis_id=delivery_basis_id,
        )
        stmt = stmt.order_by(SpimexTradingResult.date.asc(), SpimexTradingResult.id.asc())
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_trading_results(
        self,
        oil_id: str | None = None,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
        limit: int = 100,
    ) -> list[SpimexTradingResult]:
        stmt: Select[tuple[SpimexTradingResult]] = select(SpimexTradingResult)
        stmt = self._apply_filters(
            stmt=stmt,
            oil_id=oil_id,
            delivery_type_id=delivery_type_id,
            delivery_basis_id=delivery_basis_id,
        )
        stmt = stmt.order_by(SpimexTradingResult.date.desc(), SpimexTradingResult.id.desc()).limit(
            limit
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[SpimexTradingResult]],
        oil_id: str | None,
        delivery_type_id: str | None,
        delivery_basis_id: str | None,
    ) -> Select[tuple[SpimexTradingResult]]:
        if oil_id is not None:
            stmt = stmt.where(SpimexTradingResult.oil_id == oil_id)
        if delivery_type_id is not None:
            stmt = stmt.where(SpimexTradingResult.delivery_type_id == delivery_type_id)
        if delivery_basis_id is not None:
            stmt = stmt.where(SpimexTradingResult.delivery_basis_id == delivery_basis_id)
        return stmt
