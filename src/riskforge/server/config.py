"""Server configuration via pydantic-settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class ServerConfig(BaseSettings):
    secret_key: str = ""
    storage_backend: str = "filesystem"
    project_dir: str = "."
    cors_origins: list[str] = []
    rate_limit_per_minute: int = 1000

    model_config = {"env_prefix": "RISKFORGE_"}
