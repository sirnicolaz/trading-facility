from unittest import TestCase
from unittest.mock import patch
from data.api.conversion_utilities import convert_orders_to_btc


class TestConversionUtilities(TestCase):
    @patch("data.api.conversion_utilities.eth_to_btc")
    def test_get_gain_for_eth_exchange_base_case(self, mock_eth_to_btc):
        mock_eth_to_btc.return_value = 0.05
        orders = [{
            'Exchange': 'ETH-OMG',
            'Closed': '2017-09-04T07:51:24.79',
            'Price': 0.015,
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.003
        }]

        expected_result = [{
            'Exchange': 'BTC-OMG',
            'Closed': '2017-09-04T07:51:24.79',
            'Price': 0.00075,
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.000150
        }]

        result = convert_orders_to_btc(orders)

        self.assertListEqual(expected_result, result)

    @patch("data.api.conversion_utilities.eth_to_btc")
    def test_get_gain_for_eth_exchange_base_case(self, mock_eth_to_btc):
        mock_eth_to_btc.return_value = 0.05
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
