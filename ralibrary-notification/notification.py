from datetime import datetime, timedelta
import dateutil.parser
import os
import requests


class Notification:
    """Notification message."""

    _borrower = None
    _borrows = None
    _config = None
    _email_subject = 'RA book library reminder'
    _email_body = 'Your borrowed books will expire in 2 weeks.'

    def __init__(self, borrower, borrows, config=None):
        self._borrower = borrower
        self._borrows = borrows
        self._config = self._read_config(config)

    def reminder_in_days(self, days=14):
        reminder_borrows = []
        utcnow = datetime.utcnow()
        reminder = timedelta(days=days)
        for borrow in self._borrows:
            expected_return_time = dateutil.parser.parse(
                borrow['ExpectedReturnTime'])
            if utcnow + reminder > expected_return_time:
                reminder_borrows.append(borrow)
        self._notify(reminder_borrows)

    def _notify(self, borrows):
        url = self._config.get('api_endpoint_mailnotification')
        timeout = self._config.get('request_timeout_seconds')
        certificate_path = self._get_certificate_path()
        payload = {
            "From":"no-reply@ranotification.ra-int.com",
            "To": [self._borrower],
            "Subject": self._email_subject,
            "Body": self._email_body
        }
        req = requests.post(url, data=payload,
                            timeout=timeout, verify=certificate_path)
        try:
            req.raise_for_status()
        except:
            raise Exception('Notification: Failed to send notification.')

    def _read_config(self, config):
        if not config or not isinstance(config, dict):
            raise Exception('Missing config.')
        if 'api_endpoint_mailnotification' not in config:
            # Check required config fields.
            raise Exception('Notification: Missing required config fields.')
        cfg = {
            'api_endpoint_mailnotification':
                config['api_endpoint_mailnotification'],
            'request_timeout_seconds':
                config.get('request_timeout_seconds', 30),
            'email_body': config.get('email_body', self._email_body),
            'email_subject': config.get('email_subject', self._email_subject)
        }
        return cfg

    def _get_certificate_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'assets',
                            'certificate.cer')
