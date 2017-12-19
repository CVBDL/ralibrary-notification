"""Logging module."""

from datetime import datetime
import logging
import os

__all__ = ['logger']


def generate_log_filename():
    """Returns the full path of a log file."""

    # '2017-12-25T18:00:00.000000' to '20171225_180000'
    current_time = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    # sample: 'ralibrary_notification.20171219_112410.log'
    filename = str.format('ralibrary_notification.{0}.log', current_time)
    fullname = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'logs', filename)
    return fullname

filename = generate_log_filename()

# set to lowest level
level = logging.DEBUG

# sample: '[2017-12-25T18:00:00] [INFO] Log file is created successfully.'
format = '[%(asctime)s] [%(levelname)s] %(message)s'

# sample: '2017-12-25T18:00:00'
datefmt = '%Y-%m-%dT%H:%M:%S'

logging.basicConfig(
    filename=filename,
    level=level,
    format=format,
    datefmt=datefmt)

logger = logging.getLogger()

logger.info('Log file is created successfully.')
