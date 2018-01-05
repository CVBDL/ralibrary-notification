from datetime import datetime
import unittest
from unittest import mock

from mock_borrows import mock_borrows
from mock_config import MockConfig
from mock_requests import mock_borrows, mocked_requests_get

from ralibrarynotification.borrowsloader import BorrowsLoader


class TestBorrowsLoader(unittest.TestCase):
    @mock.patch('requests.get',
                side_effect=mocked_requests_get)
    def test_load(self, mocked_requests_get):
        borrows = BorrowsLoader(MockConfig()).load()
        mocked_requests_get.assert_called_once()
        self.assertEqual(borrows, mock_borrows)


if __name__ == '__main__':
    unittest.main()
