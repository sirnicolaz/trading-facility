from unittest import TestCase
from unittest.mock import patch

from data.order_manager import calculate_gains


class TestOrderManager(TestCase):
    @patch("data.order_manager.get_ticker")
    @patch("data.order_manager.simplified_user_orders")
    def test_calculate_gains(self, mock_simplified_user_orders, mock_get_ticker):
        test_currency = "STORJ"
        mock_simplified_user_orders.return_value = self.__mocked_orders(test_currency)
        mock_get_ticker.return_value = {"Last": 0.8, "Ask": 0.85, "Bid": 0.76}

        result = calculate_gains(test_currency, 0.9)

        self.assertListEqual([265.625, 5.0, 245.3125, 4.6, 208.75, 3.88, 225.0, 4.2], result)

    def __mocked_orders(self, currency):
        market = "BTC-" + currency
        return [{
            'Exchange': market,
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 3,
            'PricePerUnit': 0.4
        },{
            'Exchange': market,
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 5,
            'PricePerUnit': 0.2
        }]
