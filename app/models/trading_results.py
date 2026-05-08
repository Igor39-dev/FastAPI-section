from datetime import date as dt

from sqlalchemy import Date, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SpimexTradingResult(Base):
    __tablename__ = "spimex_trading_results"

    __table_args__ = (
        Index("idx_trading_results_date", "date"),
        Index("idx_trading_results_oil_id", "oil_id"),
        Index("idx_trading_results_delivery_type_id", "delivery_type_id"),
        Index("idx_trading_results_delivery_basis_id", "delivery_basis_id"),
        Index(
            "idx_trading_results_common_filters",
            "date",
            "oil_id",
            "delivery_type_id",
            "delivery_basis_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[dt] = mapped_column(Date, nullable=False, index=True)
    oil_id: Mapped[str] = mapped_column(nullable=False, index=True)
    delivery_type_id: Mapped[str] = mapped_column(nullable=False, index=True)
    delivery_basis_id: Mapped[str] = mapped_column(nullable=False, index=True)
    volume: Mapped[float] = mapped_column(nullable=False)
    total: Mapped[float] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
