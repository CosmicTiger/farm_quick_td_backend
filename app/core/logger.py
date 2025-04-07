import logging
from enum import StrEnum

from pyfiglet import Figlet

from .settings import settings


class LogLevels(StrEnum):
    """LogLevels Enum"""

    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


f = Figlet(font="slant")

logging.basicConfig(level=settings.LOGGER_LEVEL, format=settings.LOGGER_FORMAT)
logger = logging.getLogger(__name__)

logger_file = logging.FileHandler(settings.LOGGER_FILE_NAME)
logger_file.setLevel(logging.INFO)
logger.addHandler(logger_file)


# def configure_logging(log_level: str = LogLevels.ERROR) -> None:
#     log_level = log_level.upper()
#     log_levels = [level.value for level in LogLevels]

#     if log_level not in log_levels:
#         logging.basicConfig(level=settings.LOGGER_LEVEL, format=settings.LOGGER_FORMAT)
#         return

#     if log_level == LogLevels.DEBUG:
#         logger.basicConfig(level=logging.DEBUG, format=settings.LOGGER_FORMAT)
#         return

#     logging.basicConfig(level=log_level, format=settings.LOGGER_FORMAT)
