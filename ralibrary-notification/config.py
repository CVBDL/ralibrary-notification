import json
import os


class NotificationConfig:
    """Provide global configurations.

    Args:
        file_path (str): Config file path.
    Attributes:
        config: Parsed config object.
    Example:
        cfg = NotificationConfig()
        cfg.config['request_timeout_seconds']  # Output: 30
"""

    _config = None
    _default_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'assets', 'config.jsona')

    def __init__(self, file_path=None):
        self._config = self._from_json_file(file_path)

    def _from_json_file(self, file_path):
        try:
            file_path = file_path or self._default_file_path
            with open(file_path, 'r', encoding='utf-8') as config_json:
                return json.load(config_json)
        except:
            return None

    @property
    def config(self):
        return self._config
