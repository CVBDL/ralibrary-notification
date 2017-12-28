import sys

import config
from log import logger
from borrowsloader import BorrowsLoader
from notification import Notification


if __name__ == '__main__':
    logger.info('Job started.')
    try:
        cfg = config.get_config()
        borrowsloader = BorrowsLoader(cfg)
        for borrower, borrows in BorrowsLoader.groupby_borrower(
                borrowsloader.load_about_expire()):
            try:
                notification = Notification(cfg, borrower, borrows)
                notification.send_mail()
            except Exception as e:
                logger.warn(e)
    except Exception as e:
        logger.error(e)
    logger.info('Job finished.')
