from unittest import TestCase
from unittest.mock import patch
from controllers.conversion_manager import convert_orders_to_btc, convert_orders_to_eth


class TestConversionManager(TestCase):
    @patch("controllers.conversion_manager.get_price")
    def test_get_gain_for_eth_exchange(self, mock_get_price):
        mock_get_price.return_value = 0.05
        orders = [{
            'Exchange': 'ETH-SHITCOIN',
            'Closed': '2017-09-04T07:51:24.79',
            'Price': 0.00015,
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.000003
        }]

        expected_result = [{
            'Exchange': 'BTC-SHITCOIN',
            'Closed': '2017-09-04T07:51:24.79',
            'Price': 0.0000075,
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.000000150
        }]

        result = convert_orders_to_btc(orders)

        self.assertListEqual(expected_result, result)

    @patch("controllers.conversion_manager.get_price")
    def test_get_gain_for_eth_exchange(self, mock_get_price):
        mock_get_price.return_value = 0.05
        orders = [{
            'Exchange': 'BTC-SHITCOIN',
            'Closed': '2017-09-04T07:51:24.79',
            'Price': 0.00015,
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.000003
        }]

        expected_result = [{
            'Exchange': 'ETH-SHITCOIN',
            'Closed': '2017-09-04T07:51:24.79',
            'Price': 0.0000075,
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.000000150
        }]

        result = convert_orders_to_eth(orders)

        self.assertListEqual(expected_result, result)