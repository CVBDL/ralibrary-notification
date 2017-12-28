"""Load borrows."""

from datetime import datetime, timedelta
from itertools import groupby
import dateutil.parser
import os
import requests


class BorrowsLoader:
    """Borrows data source and utils."""

    _is_loaded = False
    _borrows = None
    _config = None

    def __init__(self, config):
        self._config = config

    @staticmethod
    def groupby_borrower(borrows):
        keyfunc = lambda b: b['Borrower']
        return groupby(sorted(borrows, key=keyfunc), keyfunc)

    def load(self):
        if not self._is_loaded:
            auth = requests.auth.HTTPBasicAuth(self._config.ralibrary_username,
                                               self._config.ralibrary_password)
            req = requests.get(self._config.api_endpoint_borrows,
                               timeout=self._config.request_timeout_seconds,
                               auth=auth,
                               verify=self._get_certificate_path())
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

    def load_about_expire(self):
        if not self._is_loaded:
            self.load()
        return filter(self._is_about_expire, self._borrows)

    def load_expired(self):
        if not self._is_loaded:
            self.load()
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

    def _get_certificate_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'assets',
                            'certificate.cer')

#[
#  {
#    "Borrower": "patrick@example.com",
#    "BorrowTime": "2017-09-24T11:08:48",
#    "ExpectedReturnTime": "2017-10-24T11:08:48",
#    "Book": {
#      "Id": 2,
#      "Code": "P002",
#      "ISBN10": "7111348664",
#      "ISBN13": "9787111348665",
#      "Title": "Design",
#      "Subtitle": "",
#      "Authors": "Jesse James Garrett",
#      "Publisher": null,
#      "PublishedDate": "2011",
#      "Description": null,
#      "PageCount": 191,
#      "ThumbnailLink": null,
#      "CreatedDate": "2017-09-24T11:08:48.93",
#      "RowVersion": "AAAAAAAAF3I="
#    }
#  }
#]
