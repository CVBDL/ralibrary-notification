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

    @mock.patch('requests.get',
                side_effect=mocked_requests_get)
    def test_load_cache(self, mocked_requests_get):
        loader = BorrowsLoader(MockConfig())
        borrows_1 = loader.load()
        borrows_2 = loader.load()
        mocked_requests_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
