from unittest import TestCase
from unittest.mock import patch
from data.gain_calculator import *


class TestGainCalculator(TestCase):

    @patch("data.gain_calculator.get_order_history")
    @patch("data.gain_calculator.get_ticker")
    @patch("data.gain_calculator.get_balances")
    def test_get_all_gains(self, mock_get_balances, mock_get_ticker, mock_get_order_history):
        mock_get_balances.return_value = [{'Currency': 'OMG', 'Balance': 1.0}]
        mock_get_ticker.return_value = self.__mock_ticker()
        mock_get_order_history.return_value = [{
            'OrderType': 'LIMIT_BUY',
            'Exchange': 'BTC-OMG',
            'QuantityRemaining': 0.0,
            'Quantity': 5.0,
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.003
        }]

        gains = get_all_gains()

        self.assertEqual(1, len(gains))
        self.assertListEqual(['OMG', 100], gains[0])


    @patch("data.gain_calculator.get_order_history")
    @patch("data.gain_calculator.get_ticker")
    @patch("data.gain_calculator.get_balances")
    def test_get_gain_for_currency_with_sells(self, mock_get_balances, mock_get_ticker, mock_get_order_history):
        mock_get_balances.return_value = [{'Currency': 'OMG', 'Balance': 1.0}]
        mock_get_ticker.return_value = self.__mock_ticker()
        test_exchange = 'BTC-OMG'
        order_buy_1 = {
            'OrderType': 'LIMIT_BUY',
            'Exchange': test_exchange,
            'Quantity': 5.0,
            'QuantityRemaining': 0.0,
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.003
        }
        order_sell =  {
            'OrderType': 'LIMIT_SELL',
            'Exchange': test_exchange,
            'QuantityRemaining': 0.0,
            'Quantity': 3
        }
        order_buy_2 = {
            'OrderType': 'LIMIT_BUY',
            'Exchange': test_exchange,
            'QuantityRemaining': 0.0,
            'ActualQuantity': 4.0,
            'Quantity': 4.0,
            'PricePerUnit': 0.075
        }
        mock_get_order_history.return_value = [order_buy_1, order_sell, order_buy_2]
        expected_result = [['OMG', 68.0]]

        result = get_all_gains()

        self.assertListEqual(expected_result, result)

    def __mock_ticker(self):
        return {'Ask': 0.006, 'Bid': 0.003, 'Last': 0.006}
