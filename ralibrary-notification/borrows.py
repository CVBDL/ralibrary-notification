from itertools import groupby
from log import logger
import os
import requests


class Borrows:
    """Provide global configurations.

    Args:
        config: Config object.
    """

    _borrows=None
    _config = None

    def __init__(self, config):
        self._config = config
        self._borrows = self._fetch_borrows()

    def __iter__(self):
        return self._grouped_borrows

    @property
    def group_of_borrower(self):
        keyfunc = lambda b: b['Borrower']
        sorted_borrows = sorted(self._borrows, key=keyfunc)
        return groupby(sorted_borrows, keyfunc)

    def _fetch_borrows(self):
        auth = requests.auth.HTTPBasicAuth(self._config.ralibrary_username,
                                           self._config.ralibrary_password)
        req = requests.get(self._config.api_endpoint_borrows,
                           timeout=self._config.request_timeout_seconds,
                           auth=auth,
                           verify=self._get_certificate_path())
        try:
            req.raise_for_status()
        except:
            raise Exception('Borrows: Failed to fetch borrows.')
        try:
            return req.json()
        except:
            raise Exception('Borrows: Failed to parse borrows json.')

    def _get_certificate_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'assets',
                            'certificate.cer')
