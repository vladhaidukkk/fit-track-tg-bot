import logging
from typing import Literal

LogLevelName = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def configure_logging(level_name: LogLevelName = "INFO") -> None:
    logging.basicConfig(level=level_name)


logger = logging.getLogger("bot")
