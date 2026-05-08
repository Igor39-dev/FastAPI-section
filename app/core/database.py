from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import text

from app.core.config import settings


class Base(DeclarativeBase):
    pass



engine: AsyncEngine = create_async_engine(
    settings.DB_URL,
    echo=settings.POSTGRES_ECHO,
    pool_size=settings.POSTGRES_POOL_SIZE,
    max_overflow=settings.POSTGRES_MAX_OVERFLOW,
    pool_timeout=settings.POSTGRES_POOL_TIMEOUT,
    pool_recycle=settings.POSTGRES_POOL_RECYCLE,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

session = async_session_factory()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для выдачи асинхронной сессии БД."""

    async with async_session_factory() as session:
        yield session


async def check_db_connection() -> bool:
    """Проверяет доступность БД через простой SELECT."""

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception:
        return False
    return True
