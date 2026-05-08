from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import uvicorn
from fastapi import FastAPI

from app.core.database import check_db_connection, engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Управляет жизненным циклом приложения."""

    yield
    await engine.dispose()


app = FastAPI(
    title="Spimex Trading API",
    version="0.1.0",
    description="API для работы с данными из таблицы spimex_trading_results",
    lifespan=lifespan,
)


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """Базовый healthcheck для мониторинга сервиса."""

    db_ok = await check_db_connection()
    return {"status": "ok" if db_ok else "degraded"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
