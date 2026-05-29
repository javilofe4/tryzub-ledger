from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(".env"), env_file_encoding="utf-8")

    APP_ENV: str = Field(default="development")
    DATABASE_URL: str = Field(default="postgresql+asyncpg://tryzub:tryzub@postgres:5432/tryzub_ledger")
    REDIS_URL: str = Field(default="redis://redis:6379/0")
    ADMIN_TOKEN: str | None = Field(default=None)
    NEXT_PUBLIC_API_BASE_URL: str = Field(default="http://localhost:8000")
    AI_PROVIDER: str = Field(default="disabled")
    OPENAI_API_KEY: str | None = Field(default=None)
    MAP_TILE_URL: str = Field(default="https://tile.openstreetmap.org/{z}/{x}/{y}.png")
    AUTO_CREATE_DB: bool = Field(default=False)


settings = Settings()
