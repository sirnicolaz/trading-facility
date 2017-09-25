from unittest import TestCase
from unittest.mock import patch

from controllers.profit_calculator import get_current_profit


class TestCurrentProfitCalculator(TestCase):
    @patch("controllers.profit_calculator.get_ticker")
    @patch("controllers.profit_calculator.get_balance")
    def test_get_current_profit_base_case(self, mock_get_balance, mock_get_ticker):
        mock_get_ticker.return_value = {'Last': 0.4}
        mock_get_balance.return_value = {'Balance': 5.0}

        orders = [{
            'Exchange': 'BTC-STORJ',
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 5,
            'PricePerUnit': 0.2
        }]

        result = get_current_profit(orders, 'dummy')

        expected_result = 1
        self.assertEqual(expected_result, result)

    @patch("controllers.profit_calculator.get_ticker")
    @patch("controllers.profit_calculator.get_balance")
    def test_get_current_profit_with_history(self, mock_get_balance, mock_get_ticker):
        mock_get_ticker.return_value = {'Last': 0.4}
        mock_get_balance.return_value = {'Balance': 3.0}

        orders = [{
            'Exchange': 'BTC-STORJ',
            'OrderType': 'LIMIT_SELL',
            'ActualQuantity': 2,
            'PricePerUnit': 0.3
        },{
            'Exchange': 'BTC-STORJ',
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 5,
            'PricePerUnit': 0.2
        }]

        # 0.2 * 3 = 0.6
        # 0.4 * 3 = 1.2
        # 1.2 - 0.6 = 0.6

        result = get_current_profit(orders, 'dummy')

        expected_result = 0.6
        self.assertEqual(expected_result, result)

    @patch("controllers.profit_calculator.get_ticker")
    @patch("controllers.profit_calculator.get_balance")
    def test_get_current_profit_with_complex_history(self, mock_get_balance, mock_get_ticker):
        mock_get_ticker.return_value = {'Last': 0.4}
        mock_get_balance.return_value = {'Balance': 6.0}

        orders = [{
            'Exchange': 'BTC-STORJ',
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 3,
            'PricePerUnit': 0.4
        },{
            'Exchange': 'BTC-STORJ',
            'OrderType': 'LIMIT_SELL',
            'ActualQuantity': 2,
            'PricePerUnit': 0.3
        },{
            'Exchange': 'BTC-STORJ',
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 5,
            'PricePerUnit': 0.2
        }]

        result = get_current_profit(orders, 'dummy')

        expected_result = 0.6
        self.assertEqual(expected_result, result)

