from log import logger
import os
import requests


class Borrows:
    """Provide global configurations.

    Args:
        config: Config object.
    """

    _borrows = None
    _config = None

    def __init__(self, config=None):
        self._config = self._read_config(config)

    def _read_config(self, config):
        if not config or not isinstance(config, dict):
            raise Exception('Missing config.')
        if ('account_username' not in config or
            'account_password' not in config or
            'api_endpoint_borrows' not in config):
            # Check required config fields.
            raise Exception('Missing required config fields.')
        cfg = {
            'api_endpoint_borrows': config['api_endpoint_borrows'],
            'account_username':config['account_username'],
            'account_password': config['account_password'],
            'request_timeout_seconds': config.get('request_timeout_seconds', 30)
        }
        return cfg

    def _fetch_borrows(self):
        url = self._config.get('api_endpoint_borrows')
        username = self._config.get('account_username')
        password = self._config.get('account_password')
        auth = requests.auth.HTTPBasicAuth(username, password)
        timeout = self._config.get('request_timeout_seconds')
        certificate_path = self._get_certificate_path()
        req = requests.get(url,
                           auth=auth,
                           verify=certificate_path,
                           timeout=timeout)
        req.raise_for_status()
        return req.json()

    def _get_certificate_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'assets',
                            'certificate.cer')
