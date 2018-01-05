import dateutil.parser
from datetime import datetime, timedelta
from itertools import groupby


class Borrows:
    _borrows = None
    _config = None

    def __init__(self, config, borrows):
        if not isinstance(borrows, list):
            raise Exception('Borrows: Invalid borrows, should be a list.')
        self._borrows = borrows
        self._config = config

    @staticmethod
    def groupby_borrower(borrows):
        keyfunc = lambda b: b['Borrower']
        return groupby(sorted(borrows, key=keyfunc), keyfunc)

    def list_about_expire(self):
        return filter(self._is_about_expire, self._borrows)

    def list_expired(self):
        return filter(self._is_expired, self._borrows)

    def _is_about_expire(self, borrow: dict, threshold=None) -> bool:
        if threshold is None:
            expire_threshold = timedelta(days=self._config.reminder_days)
        else:
            expire_threshold = timedelta(days=threshold)
        utcnow = datetime.utcnow()
        expected_return_time = dateutil.parser.parse(
            borrow['ExpectedReturnTime'])
        return (utcnow + expire_threshold) >= expected_return_time

    def _is_expired(self, borrow: dict) -> bool:
        return self._is_about_expire(borrow, 0)
