from unittest import TestCase
from unittest.mock import patch
from data.api.conversion_utilities import convert_orders_to_btc


class TestConversionUtilities(TestCase):
    @patch("data.api.conversion_utilities.eth_to_btc")
    def test_get_gain_for_eth_exchange(self, mock_eth_to_btc):
        mock_eth_to_btc.return_value = 0.00032
        orders = [{
            'OrderType': 'LIMIT_BUY',
            'Exchange': 'ETH-OMG',
            'Closed': '2017-09-04T07:51:24.79',
            'Quantity': 5.0,
            'Price': 0.015,
            'QuantityRemaining': 0.0,
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.003
        }]

        expected_result = [{
            'OrderType': 'LIMIT_BUY',
            'Exchange': 'BTC-OMG',
            'Closed': '2017-09-04T07:51:24.79',
            'Quantity': 5.0,
            'Price': 0.021333333333333336,
            'QuantityRemaining': 0.0,
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.10666666666666667
        }]


        result = convert_orders_to_btc(orders)

        self.assertListEqual(expected_result, result)
