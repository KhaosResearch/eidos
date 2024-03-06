from pathlib import Path

import structlog
from pydantic_settings import BaseSettings, SettingsConfigDict

log = structlog.get_logger("eidos.settings")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=(".env", ".env.prod")
    )

    # The root path of the API. Useful when deploying the API behind a reverse proxy.
    root_path: str = ""

    # The API key to be used for authentication. You can generate a new one by running:
    # $ openssl rand -hex 32
    api_key: str = ""

    # The path to the folder containing the AI functions.
    functions_folder: Path = Path("functions")


settings = Settings()
