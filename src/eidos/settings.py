from pathlib import Path

import structlog
from pydantic_settings import BaseSettings

log = structlog.get_logger("eidos.settings")


class Settings(BaseSettings):
    # The root path of the API. Useful when deploying the API behind a reverse proxy.
    root_path: str = ""

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 6004

    api_key: str = (
        "Gosh, why am I using a default api key? I better override it "
        "with the API_KEY environment variable."
    )

    log_level: str = "info"
    functions_folder: Path = Path("functions")

    class Config:
        # Later files in the list will take priority over earlier files.
        env_file = [".env", ".env.prod"]
        for f in reversed(env_file):
            if Path(f).exists():
                log.info("Loading environment variables from file", file=f)
                break
        env_file_encoding = "utf-8"


config = Settings()
