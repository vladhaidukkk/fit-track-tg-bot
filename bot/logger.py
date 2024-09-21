import logging
import sys
from typing import Literal

import colorlog

LogLevelName = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def configure_logging(level_name: LogLevelName = "INFO") -> None:
    stdout_handler = colorlog.StreamHandler(stream=sys.stdout)
    colored_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s:%(name)s:%(log_color)s%(message)s%(reset)s"
    )
    stdout_handler.setFormatter(colored_formatter)
    logging.basicConfig(level=level_name, handlers=[stdout_handler])


logger = logging.getLogger("bot")
