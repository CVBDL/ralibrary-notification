import json
import os


class ConfigParser:
    """Provide global configurations.

    Args:
        file_path (str): Config file path.
    Attributes:
        config: Parsed config object.
    Example:
        cfg = NotificationConfig()
        cfg.config['request_timeout_seconds']  # Output: 30
    """

    _raw_config = None
    _default_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'assets', 'config.json')

    def __init__(self, file_path=None):
        self._raw_config = self._from_json_file(file_path)

    def _from_json_file(self, file_path):
        try:
            file_path = file_path or self._default_file_path
            with open(file_path, 'r', encoding='utf-8') as config_json:
                return json.load(config_json)
        except:
            return None

    @property
    def raw_config(self):
        return self._raw_config


class Config:
    """Provide config values."""

    _config = None

    def __init__(self, config=None):
        if not config or not isinstance(config, dict):
            raise Exception('Config: Cannot read config file.')
        if 'ralibrary_username' not in config:
            raise Exception(
                'Config: Missing "ralibrary_username" field.')
        if 'ralibrary_password' not in config:
            raise Exception(
                'Config: Missing "ralibrary_password" field.')
        if 'api_endpoint_borrows' not in config:
            raise Exception(
                'Config: Missing "api_endpoint_borrows" field.')
        if 'api_endpoint_mailnotification' not in config:
            raise Exception(
                'Config: Missing "api_endpoint_mailnotification" field.')
        # init config
        self._config = config

    @property
    def ralibrary_username(self):
        return self._config.get('ralibrary_username')

    @property
    def ralibrary_password(self):
        return self._config.get('ralibrary_password')

    @property
    def api_endpoint_borrows(self):
        return self._config.get('api_endpoint_borrows')

    @property
    def api_endpoint_mailnotification(self):
        return self._config.get('api_endpoint_mailnotification')

    @property
    def email_subject(self):
        subject = 'RA book library reminder'
        return self._config.get('email_subject', subject)

    @property
    def email_from(self):
        mailfrom = 'noreply@rockwellautomation.com'
        return self._config.get('email_from', mailfrom)

    @property
    def email_body(self):
        body = 'Your borrowed books will expire soon.'
        return self._config.get('email_body', body)

    @property
    def email_cc_admin(self):
        return self._config.get('email_cc_admin', [])

    @property
    def ralibrary_client(self):
        return self._config.get('ralibrary_client', '')

    @property
    def request_timeout_seconds(self):
        return self._config.get('request_timeout_seconds', 30)

    @property
    def request_interval(self):
        return self._config.get('request_interval', 2)

    @property
    def reminder_days(self):
        return self._config.get('reminder_days', 14)


def get_config():
    return Config(config=ConfigParser().raw_config)
