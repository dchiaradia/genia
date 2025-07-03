import sys

from loguru import logger

logger.remove()


logger.add(
    sys.stdout,
    # format="{level}|{time}|{message}",
    level="DEBUG",
)


def get_logger():
    return logger
