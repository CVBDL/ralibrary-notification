from datetime import datetime, timedelta
import dateutil.parser
import os
import requests


class Notification:
    """Notification message."""

    _config = None
    _borrower = None
    _borrows = None

    def __init__(self, config, borrower, borrows):
        self._config = config
        self._borrower = borrower
        self._borrows = borrows

    def remind_in_days(self, days=None):
        if days is None:
            days = self._config.reminder_days
        reminder_borrows = []
        utcnow = datetime.utcnow()
        reminder = timedelta(days=days)
        for borrow in self._borrows:
            expected_return_time = dateutil.parser.parse(
                borrow['ExpectedReturnTime'])
            if utcnow + reminder > expected_return_time:
                reminder_borrows.append(borrow)
        self._send(reminder_borrows)

    def _send(self, borrows):
        # Doc: https://github.com/CVBDL/RaNotification
        payload = {
            "From": self._config.email_from,
            "To": [self._borrower],
            "Subject": self._config.email_subject,
            "Body": self._config.email_body
        }
        try:
            req = requests.post(self._config.api_endpoint_mailnotification,
                                data=payload,
                                timeout=self._config.request_timeout_seconds,
                                verify=self._get_certificate_path())
            req.raise_for_status()
        except:
            raise Exception(str.format('Notification: Failed to notify {0}',
                                       self._borrower))

    def _get_certificate_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'assets',
                            'certificate.cer')
