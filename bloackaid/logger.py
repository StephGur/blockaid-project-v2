import logging
import os
from logging import Logger

from flask import current_app
from werkzeug.local import LocalProxy

logger: Logger = LocalProxy(lambda: current_app.logger)


def get_logging_level():
    level_name = os.environ.get('LOG_LEVEL')
    if level_name:
        return logging.getLevelName(level_name)
