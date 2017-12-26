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

    def __init__(self, config=None):
        #self._config = self._read_config(config)
        #self._borrows = self._fetch_borrows()
        self._borrows = [{
          "Borrower": "pzhong@ra.rockwell.com",
          "BorrowTime": "2017-09-24T05:33:46.007",
          "ExpectedReturnTime": "2017-12-23T05:33:46.007",
          "Book": {
              "Title": "Java"
          }
        }, {
          "Borrower": "pzhong@ra.rockwell.com",
          "BorrowTime": "2017-11-24T05:33:46.007",
          "ExpectedReturnTime": "2018-02-11T05:33:46.007",
          "Book": {
              "Title": "C++"
          }
        }]

    def __iter__(self):
        return self._grouped_borrows

    def _read_config(self, config):
        if not config or not isinstance(config, dict):
            raise Exception('Missing config.')
        if ('account_username' not in config or
            'account_password' not in config or
            'api_endpoint_borrows' not in config):
            # Check required config fields.
            raise Exception('Borrows: Missing required config fields.')
        cfg = {
            'api_endpoint_borrows': config['api_endpoint_borrows'],
            'account_username':config['account_username'],
            'account_password': config['account_password'],
            'request_timeout_seconds': config.get('request_timeout_seconds', 30)
        }
        return cfg

    def _fetch_borrows(self):
        url = self._config.get('api_endpoint_borrows')
        timeout = self._config.get('request_timeout_seconds')
        username = self._config.get('account_username')
        password = self._config.get('account_password')
        auth = requests.auth.HTTPBasicAuth(username, password)
        certificate_path = self._get_certificate_path()
        req = requests.get(url, timeout=timeout,
                           auth=auth, verify=certificate_path)
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

    @property
    def group_of_borrower(self):
        keyfunc = lambda b: b['Borrower']
        sorted_borrows = sorted(self._borrows, key=keyfunc)
        return groupby(sorted_borrows, keyfunc)
