class MessageFormatter:
    """Formatting notification message."""

    _borrows = None
    _config = None

    def __init__(self, config, borrows):
        self._borrows = borrows
        self._config = config

    def serialize(self):
        return {
            'title': self._serialize_title(),
            'body': self._serialize_body()
        }

    def serialize_expired(self):
        return {
            'title': self._serialize_title(),
            'body': self._serialize_body_expired()
        }

    def _serialize_title(self):
        return self._config.email_subject

    def _serialize_body(self):
        body = '<p>The following books are <strong>about to expire</strong>:</p>'
        body += '<ol>'
        for borrow in self._borrows:
            body += str.format('<li><u>{0}</u> / {1} / Expire Date: {2}</li>',
                               borrow['Book']['Title'],
                               borrow['Book']['Code'],
                               borrow['ExpectedReturnTime'])
        body += '</ol>'
        body += str.format(
            '<p>View it in RA book library client: '
            '<a href="{0}" target="_blank">{0}</a></p>',
            self._config.ralibrary_client)
        return body

    def _serialize_body_expired(self):
        body = '<p>The following books are <strong>expired</strong>:</p>'
        body += '<ol>'
        for borrow in self._borrows:
            body += str.format('<li><u>{0}</u> / {1} / Expire Date: {2}</li>',
                               borrow['Book']['Title'],
                               borrow['Book']['Code'],
                               borrow['ExpectedReturnTime'])
        body += '</ol>'
        body += str.format(
            '<p>View it in RA book library client: '
            '<a href="{0}" target="_blank">{0}</a></p>',
            self._config.ralibrary_client)
        return body
