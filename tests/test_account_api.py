from unittest import TestCase
from api.account_api import get_order_history


# TODO: this uses the actualy APIs with key and secret.
# Make sure at some point that the web calls are mocked out

class TestAccountAPI(TestCase):
    def test_get_order_history_no_market(self):
        data = get_order_history()
        self.assertGreater(len(data), 0)

    def test_get_order_history_with_market(self):
        data = get_order_history("BTC-NEO")
        self.assertGreater(len(data), 0)
