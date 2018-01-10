import requests

from ralibrarynotification.certificate import Certificate


class MailNotificationError(Exception):
    pass


class MailNotification:
    """Send notifications via e-mail."""

    _config = None
    _msg = None
    _to = None
    _cc = None
    _bcc = None
    _from = None

    def __init__(self, config, to, msg, cc=None, bcc=None, from_=None):
        self._config = config
        self._msg = msg
        if not isinstance(to, list):
            to = [to]
        self._to = to
        self._cc = cc or []
        self._bcc = bcc or []
        self._from = from_ or self._config.email_from

    def send(self):
        try:
            req = requests.post(self._config.api_endpoint_mailnotification,
                                data=self._get_payload(),
                                timeout=self._config.request_timeout_seconds,
                                verify=Certificate.get_path())
            req.raise_for_status()
        except:
            raise MailNotificationError(
                str.format('Notification: Failed to notify {0}',
                           self._borrower))

    def _get_payload(self):
        # Doc: https://github.com/CVBDL/RaNotification
        return {
            'From': self._from,
            'To': self._to,
            'Cc': self._cc,
            'Bcc': self._bcc,
            'Subject': self._msg.get('title', ''),
            'Body': self._msg.get('body', ''),
            'IsHtml': True
        }
