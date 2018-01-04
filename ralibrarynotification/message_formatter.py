class MessageFormatter:
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

    def _serialize_title(self):
        return self._config.email_subject

    def _serialize_body(self):
        body = 'The following books are about to expire:\n\n'
        for borrow in self._borrows:
            body += str.format('- {0} / {1} / Expire Date: {2}\n',
                               borrow['Book']['Title'],
                               borrow['Book']['Code'],
                               borrow['ExpectedReturnTime'])
        body += str.format('\n\nView it in RA book library client: {0}\n',
                           self._config.ralibrary_client)
        return body
