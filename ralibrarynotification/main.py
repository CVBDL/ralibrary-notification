"""Main module of script."""

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
        else:
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
        else:
            logger.info(str.format('Reminding books expired to <{0}>...Done',
                                   borrower))


def main():
    """Main function.

    Workflow:
        1. Read config file.
        2. Fetch borrows data.
        3. Notify borrowers if their books are about to expire.
        3. Notify borrowers if their books are already expired.

    Q: When is "about to expire"?
    A: Say "reminder days" config is set to 14 days.
       Say one borrowed book's expected return date is 2018-01-29.
       Say today is 2018-01-15, 14 days before expected return date.
       Then, today is "about to expire", ONLY today.
       It'll ensure we only notify once instead of every day.

    Q: When is "expired"?
    A: Say "reminder days" config is set to 14 days.
       Say one borrowed book's expected return date is 2018-01-29.
       Say today is 2018-01-29.
       Then, today is "expired", ONLY today.
       It'll ensure we only notify once instead of every day.
    """
    logger.info('Script started running.')

    try:
        logger.info('Processing config...')
        cfg = config.get_config()
        logger.info('Current config options:')
        logger.info(str.format('- RA library endpoint: {0}',
                               cfg.api_endpoint_borrows))
        logger.info(str.format('- Mail notification endpoint: {0}',
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
