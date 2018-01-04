import unittest
from unittest import mock

from ralibrarynotification.borrowsloader import BorrowsLoader
from .mock_config import MockConfig
from .mock_requests import mock_borrows, mocked_requests_get


class TestBorrowsLoader(unittest.TestCase):
    @mock.patch('requests.get',
                side_effect=mocked_requests_get)
    def test_load(self, mocked_requests_get):
        borrows = BorrowsLoader(MockConfig()).load()

        mocked_requests_get.assert_called_once()
        self.assertEqual(borrows, mock_borrows)


if __name__ == '__main__':
    unittest.main()
