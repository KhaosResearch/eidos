from pathlib import Path

from pydantic_settings import BaseSettings

from eidos.logs import get_logger

logger = get_logger()


class Settings(BaseSettings):
    # The root path of the API. Useful when deploying the API behind a reverse proxy.
    root_path: str = ""

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 6004
    log_level: str = "info"
    functions_folder: Path = Path("functions")

    class Config:
        # Later files in the list will take priority over earlier files.
        env_file = [".env", ".env.prod"]
        for f in reversed(env_file):
            if Path(f).exists():
                logger.info(f"Loading environment variables from file {f}")
                break
        env_file_encoding = "utf-8"


config = Settings()
