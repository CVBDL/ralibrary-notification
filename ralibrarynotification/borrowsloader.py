import dateutil.parser
import os
import requests
from ralibrarynotification.certificate import Certificate


class BorrowsLoader:
    """Borrows data source and utils."""

    _is_loaded = False
    _borrows = None
    _config = None

    def __init__(self, config):
        self._config = config

    def load(self):
        if not self._is_loaded:
            auth = requests.auth.HTTPBasicAuth(self._config.ralibrary_username,
                                               self._config.ralibrary_password)
            req = requests.get(self._config.api_endpoint_borrows,
                               timeout=self._config.request_timeout_seconds,
                               auth=auth,
                               verify=Certificate.get_path())
            try:
                req.raise_for_status()
            except:
                raise Exception('BorrowsLoader: Failed to fetch borrows.')
            try:
                self._borrows = req.json()
            except:
                raise Exception('BorrowsLoader: Failed to parse borrows json.')
            self._is_loaded = True
        # list of all borrows
        return self._borrows
