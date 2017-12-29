import os


class Certificate:
    """Certificate manager."""

    @staticmethod
    def get_path():
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'assets',
                            'certificate.cer')
