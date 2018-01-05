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

    def test_list_about_expire(self):
        cfg = MockConfig()
        mock_borrows_data = [
            # expire
            mock_borrows.make_borrow(days_ago=0),
            # about expire
            mock_borrows.make_borrow(days_ago=-cfg.reminder_days),
            # expire
            mock_borrows.make_borrow(days_ago=cfg.reminder_days+100),
            mock_borrows.make_borrow(days_ago=-cfg.reminder_days-100)
        ]
        borrows = Borrows(cfg, mock_borrows_data)
        self.assertEqual(sum(1 for _ in borrows.list_about_expire()), 3)

    def test_list_expired_1(self):
        cfg = MockConfig()
        mock_borrows_data = [
            # expire
            mock_borrows.make_borrow(days_ago=0),
            # about expire
            mock_borrows.make_borrow(days_ago=-cfg.reminder_days),
            # expire
            mock_borrows.make_borrow(days_ago=cfg.reminder_days+100),
            mock_borrows.make_borrow(days_ago=-cfg.reminder_days-100)
        ]
        borrows = Borrows(cfg, mock_borrows_data)
        self.assertEqual(sum(1 for _ in borrows.list_expired()), 2)

    def test_list_expired_2(self):
        cfg = MockConfig()
        mock_borrows_data = [
            mock_borrows.make_borrow(days_ago=-cfg.reminder_days-1)
        ]
        borrows = Borrows(cfg, mock_borrows_data)
        self.assertEqual(sum(1 for _ in borrows.list_expired()), 0)


if __name__ == '__main__':
    unittest.main()
