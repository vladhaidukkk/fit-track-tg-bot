import logging
import logging.config
from typing import Literal

LogLevelName = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def get_logging_config(root_level_name: LogLevelName = "INFO") -> dict[str, any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(levelname)s%(reset)s:%(name)s:%(log_color)s%(message)s%(reset)s",
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "formatter": "colored",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "root": {
                "level": root_level_name,
                "handlers": ["stdout"],
            }
        }
    }


def configure_logging(level_name: LogLevelName = "INFO") -> None:
    config = get_logging_config(root_level_name=level_name)
    logging.config.dictConfig(config)


logger = logging.getLogger("bot")
