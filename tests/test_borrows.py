import unittest

import mock_borrows
from mock_config import MockConfig

from ralibrarynotification.borrows import Borrows


class TestBorrows(unittest.TestCase):
    def test_ctor_fail(self):
        with self.assertRaises(Exception):
            Borrows(MockConfig(), None)

    def test_ctor_ok(self):
        try:
            Borrows(MockConfig(), [])
        except:
            self.fail()

    def test_list_by_remaining_days(self):
        borrows = Borrows(MockConfig(), [
            mock_borrows.make_borrow(-1),
            mock_borrows.make_borrow(-1),
            mock_borrows.make_borrow(0),
            mock_borrows.make_borrow(1)])
        self.assertEqual(2, sum(1 for _ in borrows.list_by_remaining_days(1)))
        self.assertEqual(1, sum(1 for _ in borrows.list_by_remaining_days(0)))
        self.assertEqual(1, sum(1 for _ in borrows.list_by_remaining_days(-1)))
        self.assertEqual(0, sum(1 for _ in borrows.list_by_remaining_days(7)))


if __name__ == '__main__':
    unittest.main()
