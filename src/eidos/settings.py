from enum import Enum
from pathlib import Path

import structlog
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

log = structlog.get_logger("eidos.settings")


class Environment(str, Enum):
    development = "development"
    production = "production"


class Settings(BaseSettings):
    env: Environment = Environment.development

    # The root path of the API. Useful when deploying the API behind a reverse proxy.
    root_path: str = ""

    # The API key to be used for authentication. You can generate a new one by running:
    # $ openssl rand -hex 32
    api_key: str = ""

    # The path to the folder containing the AI functions.
    functions_folder: Path = Path("functions")

    model_config = SettingsConfigDict(
        env_prefix="eidos_",
        # `.env.prod` takes priority over `.env`
        env_file=(".env", ".env.prod"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("root_path")
    @classmethod
    def root_path_must_not_end_with_slash(cls, v: str) -> str:
        if v.endswith("/"):
            raise ValueError('must not end with "/"')
        return v

    def is_production(self) -> bool:
        return self.env == Environment.production


settings = Settings()
