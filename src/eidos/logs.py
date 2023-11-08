import logging.config


def configure_logging(config: dict | None = None) -> None:
    """Configure logging for the application.

    Args:
        config (dict|None): Logging configuration. If not provided, uses a default
            console logger.
    """

    DEFAULT_LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "basic": {
                "format": "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "formatter": "basic",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "eidos": {
                "level": "INFO",
                "handlers": ["console"],
            },
        },
    }

    try:
        logging.config.dictConfig(config or DEFAULT_LOGGING_CONFIG)
    except FileNotFoundError as err:
        logging.error(f"Error while configuring logging: {err}")


def get_logger(module: str = "eidos", name: str = None) -> logging.Logger:
    """Get a logger for the given module.

    Args:
        module (str): Name of the module to get the logger for.
        name (str): Name of the logger to get.

    Returns:
        logging.Logger: Logger for the given module.
    """
    logger_name = module
    if name is not None:
        logger_name += "." + name
    return logging.getLogger(logger_name)
