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


if __name__ == '__main__':
    unittest.main()
