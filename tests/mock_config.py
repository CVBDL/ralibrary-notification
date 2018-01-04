class MockConfig:
    @property
    def ralibrary_username(self):
        return ''

    @property
    def ralibrary_password(self):
        return ''

    @property
    def api_endpoint_borrows(self):
        return ''

    @property
    def api_endpoint_mailnotification(self):
        return ''

    @property
    def email_subject(self):
        return 'RA book library reminder'

    @property
    def email_from(self):
        return 'noreply@rockwellautomation.com'

    @property
    def email_body(self):
        return 'Your borrowed books will expire soon.'

    @property
    def ralibrary_client(self):
        return ''

    @property
    def request_timeout_seconds(self):
        return 30

    @property
    def request_interval(self):
        return 2

    @property
    def reminder_days(self):
        return 14
