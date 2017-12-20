"""Logging module."""

from datetime import datetime
import logging
import os

__all__ = ['logger']


class NotificationLogger:
    """Use internal logging module.

    Args:
        logging: Internal logging module.
    Attributes:
        logger: Logger object.
    """

    _logger = None

    def __init__(self, logging):
        self._config_logging(logging)
        self._logger = logging.getLogger()

    def _generate_log_filename(self):
        """Returns the full path of a log file."""
        # '2017-12-25T18:00:00.000000' to '20171225_180000'
        current_time = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        # sample: 'ralibrary_notification.20171219_112410.log'
        filename = str.format('ralibrary_notification.{0}.log', current_time)
        fullname = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'logs', filename)
        return fullname

    def _config_logging(self, logging):
        filename = self._generate_log_filename()
        # set to lowest level
        level = logging.DEBUG
        # sample: '[2017-12-25T18:00:00] [INFO] Log file is created successfully.'
        msg_format = '[%(asctime)s] [%(levelname)s] %(message)s'
        # sample: '2017-12-25T18:00:00'
        datefmt = '%Y-%m-%dT%H:%M:%S'

        logging.basicConfig(
            filename=filename,
            level=level,
            format=msg_format,
            datefmt=datefmt)

    @property
    def logger(self):
        return self._logger


class NotificationFallbackLogger():
    """Fallback logging module, provides basic APIs."""

    def debug(self, msg):
        """Fallback: logging.debug()."""
        self._log('DEBUG', msg)

    def info(self, msg):
        """Fallback: logging.info()."""
        self._log('INFO', msg)

    def warn(self, msg):
        """Fallback: logging.warn()."""
        self._log('WARNNING', msg)

    def warning(self, msg):
        """Fallback: logging.waring()."""
        self._log('WARNNING', msg)

    def error(self, msg):
        """Fallback: logging.error()."""
        self._log('ERROR', msg)

    def critical(self, msg):
        """Fallback: logging.critical()."""
        self._log('CRITICAL', msg)

    def _log(self, level, msg):
        print(str.format('[{0}] {1}', level, msg))


# singleton logger accross this app
try:
    logger = NotificationLogger(logging).logger
except:
    logger = NotificationFallbackLogger()

logger.info('Log file is created successfully.')
