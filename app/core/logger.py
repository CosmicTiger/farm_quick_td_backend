import logging

from pyfiglet import Figlet

from .settings import settings

f = Figlet(font="slant")

logging.basicConfig(level=settings.LOGGER_LEVEL, format=settings.LOGGER_FORMAT)
logger = logging.getLogger(__name__)

logger_file = logging.FileHandler(settings.LOGGER_FILE_NAME)
logger_file.setLevel(logging.INFO)
logger.addHandler(logger_file)
