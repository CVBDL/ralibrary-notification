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

    def list_by_remaining_days(self, days):
        filter_fn = lambda borrow: self._calc_remaining_days(borrow) == days
        #filter_fn = lambda b: True  # for test use
        return filter(filter_fn, self._borrows)

    def _calc_remaining_days(self, borrow: dict):
        utcnow = datetime.utcnow()
        expected_return_time = dateutil.parser.parse(
            borrow['ExpectedReturnTime'])
        delta = expected_return_time - utcnow
        return delta.days
