import sys

import config
from log import logger
from borrows import Borrows
from notification import Notification


if __name__ == '__main__':
    logger.info('Job started.')

    try:
        cfg = config.get_config()
        borrows = Borrows(cfg)
        for key, group in borrows.group_of_borrower:
            try:
                notification = Notification(cfg, key, group)
                notification.remind_in_days()
            except Exception as e:
                logger.warn(e)
    except Exception as e:
        logger.error(e)

    logger.info('Job finished.')
