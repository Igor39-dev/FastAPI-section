from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TradingDateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date


class TradingResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date
    oil_id: int
    delivery_type_id: int
    delivery_basis_id: int
    volume: float
    total: float
    count: int


class TradingDynamicsQuery(BaseModel):
    start_date: date
    end_date: date
    oil_id: int | None = None
    delivery_type_id: int | None = None
    delivery_basis_id: int | None = None

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, end_date: date, info: Any) -> date:
        start_date: date | None = info.data.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("end_date must be greater than or equal to start_date")
        return end_date


class TradingResultsQuery(BaseModel):
    oil_id: int | None = None
    delivery_type_id: int | None = None
    delivery_basis_id: int | None = None
    limit: int = Field(default=100, ge=1, le=1000)
