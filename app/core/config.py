from functools import lru_cache
from typing import Final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    POSTGRES_ECHO: bool = Field(default=False)
    POSTGRES_POOL_SIZE: int = Field(default=10, ge=1)
    POSTGRES_MAX_OVERFLOW: int = Field(default=20, ge=0)
    POSTGRES_POOL_TIMEOUT: int = Field(default=30, ge=1)
    POSTGRES_POOL_RECYCLE: int = Field(default=3600, ge=1)

    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    CACHE_TIMEZONE: str = Field(default="Europe/Moscow")

    @property
    def DB_URL(self) -> str:

        return (
            "postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


CACHE_RESET_HOUR: Final[int] = 14
CACHE_RESET_MINUTE: Final[int] = 11


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Возвращает кэшированный экземпляр настроек."""

    return Settings()


settings = Settings()
