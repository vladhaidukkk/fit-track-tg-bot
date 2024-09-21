"""Initializes a logger for the core business logic of the application.

This module initializes a logger for events related to the application's core business logic.
It functions as a third-party logger and does not include any configuration settings.
Any configuration, such as setting log levels, handlers, or formatters, should be done at the application level,
not within this module or the core business logic.

"""

import logging

logger = logging.getLogger("core")
