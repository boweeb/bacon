import logging.config
import os
import sys
from typing import Dict

from rich.console import Console
from rich.traceback import install as rich_traceback_install


RICH_CONSOLE = Console(file=sys.stderr, log_time=False, width=120)
TRUTHY = ["1", "t", "true", "y", "yes"]


def shim_env_vars(config_data: Dict):
    """Mutates logging configuration dictionary in-place before it is loaded ie. early.

    Args:
        config_data: Configuration dictionary destined for logging.config.dictConfig().

    Environment Variables:
        BACON_DEBUG:           STDOUT debug level
        BACON_DEV:             Use "rich" handler

    """

    # Force DEBUG level logging
    if "BACON_DEBUG" in os.environ.keys():
        if os.environ["BACON_DEBUG"].lower() in TRUTHY:
            config_data["handlers"]["console"]["level"] = "DEBUG"

    # Use 'rich.logging.RichHandler' with stdout (instead of 'logging.StreamHandler')
    if "BACON_DEV" in os.environ.keys():
        if os.environ["BACON_DEV"].lower() in TRUTHY:
            config_data["root"]["handlers"] = ["rich"]
            config_data["handlers"]["rich"]["level"] = "DEBUG"


LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
        "rich_fmt": {
            "format": "%(message)s <%(name)s.%(funcName)s()>",
            # Dirty hack to disable date/time column,
            "datefmt": " ",
            # datefmt: '%F %r',
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": sys.stderr,
        },
        "rich": {
            "class": "rich.logging.RichHandler",
            "level": "INFO",
            "formatter": "rich_fmt",
            "console": RICH_CONSOLE,
        },
    },
    "loggers": {
        "bacon.cli": {"propagate": "yes"},
        "bacon.bacon": {"propagate": "yes"},
        "requests": {"propagate": "no"},
        "urllib3": {"propagate": "no"},
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}

shim_env_vars(LOG_CONFIG)
logging.config.dictConfig(LOG_CONFIG)

rich_traceback_install(console=RICH_CONSOLE)
