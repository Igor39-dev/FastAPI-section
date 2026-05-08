import asyncio
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import redis.asyncio as redis_async
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from redis.exceptions import RedisError
from starlette.requests import Request

from app.api.v1.routers.trading_results import router as trading_router
from app.cache.scheduler import cache_flush_scheduler
from app.cache.service import TradingCache
from app.core.config import settings
from app.core.database import check_db_connection, engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Управляет жизненным циклом приложения."""

    redis_client = redis_async.from_url(settings.REDIS_URL, decode_responses=True)
    app.state.redis = redis_client
    app.state.trading_cache = TradingCache(
        redis_client,
        timezone=settings.CACHE_TIMEZONE,
    )

    stop_flush = asyncio.Event()
    flush_task = asyncio.create_task(
        cache_flush_scheduler(redis_client, settings.CACHE_TIMEZONE, stop_flush)
    )
    try:
        yield
    finally:
        stop_flush.set()
        flush_task.cancel()
        try:
            await flush_task
        except asyncio.CancelledError:
            pass
        await redis_client.aclose()
        await engine.dispose()


app = FastAPI(
    title="Spimex Trading API",
    version="0.1.0",
    description="API для работы с данными из таблицы spimex_trading_results",
    lifespan=lifespan,
)

app.include_router(trading_router)


@app.exception_handler(ValidationError)
async def pydantic_validation_handler(_request: Request, exc: ValidationError) -> JSONResponse:
    """Depends(Pydantic-модель) может поднимать ValidationError вне стандартного контура 422."""

    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(exc.errors())},
    )


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, object]:
    """Базовый healthcheck для мониторинга сервиса."""

    db_ok = await check_db_connection()
    redis_ok = True
    try:
        await app.state.redis.ping()
    except (RedisError, AttributeError, RuntimeError, OSError):
        redis_ok = False
    except Exception:
        redis_ok = False

    status = "ok" if db_ok and redis_ok else "degraded"
    return {
        "status": status,
        "services": {
            "database": "ok" if db_ok else "down",
            "redis": "ok" if redis_ok else "down",
        },
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
