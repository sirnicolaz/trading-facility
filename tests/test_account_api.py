from unittest import TestCase

from data.api.account_api import *


class TestAccountAPI(TestCase):
    def test_get_order_history_no_market(self):
        data = get_order_history()
        self.assertGreater(len(data), 0)

    def test_get_order_history_with_market(self):
        data = get_order_history("BTC-ETH")
        self.assertGreater(len(data), 0)
