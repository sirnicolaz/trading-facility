from unittest import TestCase
from unittest.mock import patch
from data.gain_calculator import *


class TestGainCalculator(TestCase):

    @patch("data.gain_calculator.get_ticker")
    def test_get_all_gains(self, mock_get_ticker):
        mock_get_ticker.return_value = self.__mock_ticker()
        orders = [{
            'OrderType': 'LIMIT_BUY',
            'Exchange': 'BTC-OMG',
            'QuantityRemaining': 0.0,
            'Quantity': 5.0,
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.003
        }]

        result = get_current_gain(orders)

        self.assertEqual(100, result)


    @patch("data.gain_calculator.get_ticker")
    def test_get_gain_for_currency_with_sells(self, mock_get_ticker):
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
            'ActualQuantity': 3.0,
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
        orders = [order_buy_1, order_sell, order_buy_2]

        result = get_current_gain(orders)

        self.assertEqual(68.0, result)

    def __mock_ticker(self):
        return {'Ask': 0.006, 'Bid': 0.003, 'Last': 0.006}
