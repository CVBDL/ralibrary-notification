import sys
import time

from ralibrarynotification import config
from ralibrarynotification.borrows import Borrows
from ralibrarynotification.borrowsloader import BorrowsLoader
from ralibrarynotification.log import logger
from ralibrarynotification.message_formatter import MessageFormatter
from ralibrarynotification.mailnotification import MailNotification, MailNotificationError


def _remind_about_to_expire(cfg, borrows):
    """Remind at the day before expiration time."""
    selected_borrows = borrows.list_by_remaining_days(cfg.reminder_days)
    for borrower, items in Borrows.groupby_borrower(selected_borrows):
        logger.info(str.format('Reminding books about to expire to <{0}>...',
                               borrower))
        try:
            msg = MessageFormatter(cfg, items).serialize()
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
        logger.info(str.format('Reminding books about to expire to <{0}>...Done',
                               borrower))


def _remind_expired(cfg, borrows):
    """Remind at the expire date."""
    selected_borrows = borrows.list_by_remaining_days(0)
    for borrower, items in Borrows.groupby_borrower(selected_borrows):
        logger.info(str.format('Reminding books expired to <{0}>...',
                               borrower))
        try:
            msg = MessageFormatter(cfg, items).serialize_expired()
        except Exception as e:
            raise Exception(str.format('MessageFormatter: {0}', e))
        try:
            notification = MailNotification(cfg, borrower, msg,
                                            cc=cfg.email_cc_admin)
            time.sleep(cfg.request_interval)
            notification.send()
        except MailNotificationError as e:
            # continue running
            logger.warn(e)
        except Exception as e:
            raise Exception(str.format('MailNotification: {0}', e))
        logger.info(str.format('Reminding books expired to <{0}>...Done',
                               borrower))


def main():
    logger.info('Script started running.')

    try:
        logger.info('Processing config...')
        cfg = config.get_config()
        logger.info('Current config options:')
        logger.info(str.format('- RA library endpoint: {0}',
                               cfg.api_endpoint_borrows))
        logger.info(str.format('- Main notification endpoint: {0}',
                               cfg.api_endpoint_mailnotification))
        logger.info(str.format('- Reminder days: {0}',
                               cfg.reminder_days))
        logger.info('Processing config...Done')

        logger.info('Loading borrows data...')
        borrows_data = BorrowsLoader(cfg).load()
        logger.info(str.format('Total {0} borrow records found.',
                               len(borrows_data)))
        logger.info('Loading borrows data...Done')

        logger.info('Initializing borrows...')
        borrows = Borrows(cfg, borrows_data)
        logger.info('Initializing borrows...Done')

        try:
            logger.info('Job "Remind about to expire" started running...')
            _remind_about_to_expire(cfg, borrows)
            logger.info('Job "Remind about to expire" started running...Done')
        except Exception as e:
            logger.warn('Job "Remind about to expire" stopped due to error.')
            logger.error(e)

        try:
            logger.info('Job "Remind expired" started running...')
            _remind_expired(cfg, borrows)
            logger.info('Job "Remind expired" started running...Done')
        except Exception as e:
            logger.warn('Job "Remind expired" stopped due to error.')
            logger.error(e)

    except Exception as e:
        logger.warn('Job terminated due to error.')
        logger.error(e)

    logger.info('Script finished running.')
