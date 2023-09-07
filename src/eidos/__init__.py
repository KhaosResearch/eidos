from importlib.metadata import version

from eidos.logs import configure_logging, get_logger

configure_logging()

__version__ = version("eidos")

if __name__ == "__main__":
    logger = get_logger()
    logger.info("Starting eidos...")
