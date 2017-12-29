import sys
import time

import config
from borrowsloader import BorrowsLoader
from log import logger
from message_formatter import MessageFormatter
from mailnotification import MailNotification, MailNotificationError


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
