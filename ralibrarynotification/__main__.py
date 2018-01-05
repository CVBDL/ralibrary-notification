import sys
import os

# Add project top level directory to search path.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..'))

import time

from ralibrarynotification import config
from ralibrarynotification.borrowsloader import BorrowsLoader
from ralibrarynotification.log import logger
from ralibrarynotification.message_formatter import MessageFormatter
from ralibrarynotification.mailnotification import MailNotification, MailNotificationError


if __name__ == '__main__':
    logger.info('Job started.')
    try:
        cfg = config.get_config()
        borrowsloader = BorrowsLoader(cfg)
        for borrower, borrows in BorrowsLoader.groupby_borrower(
                borrowsloader.load_about_expire()):
            try:
                msg = MessageFormatter(cfg, borrows).serialize()
            except Exception as e:
                raise Exception(str.format('MessageFormatter: {0}', e))
            try:
                notification = MailNotification(cfg, borrower, msg)
                time.sleep(cfg.request_interval)
                notification.send()
            except MailNotificationError as e:
                # continue running
                logger.warn(e)
            except Exception as e:
                raise Exception(str.format('MailNotification: {0}', e))
    except Exception as e:
        logger.warn('Job terminated due to error.')
        logger.error(e)
    logger.info('Job finished.')
