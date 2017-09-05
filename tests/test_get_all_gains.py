from unittest import TestCase
from unittest.mock import patch

from data.dashboard_data import *


class TestGet_all_gains(TestCase):
    @patch("dashboard_data.get_order_history")
    @patch("dashboard_data.get_ticker")
    @patch("dashboard_data.get_balances")
    def test_get_all_gains(self, mock_get_balances, mock_get_ticker, mock_get_order_history):
        mock_get_balances.return_value = [{'Currency': 'OMG', 'Balance': 1.0}]
        mock_get_ticker.return_value = self.__mock_ticker()
        mock_get_order_history.return_value = self.__mock_orders('OMG')

        gains = get_all_gains()

        self.assertEqual(1, len(gains))
        self.assertListEqual(['OMG', 100], gains[0])

    @patch("dashboard_data.get_ticker")
    def test_get_gain_for_currency(self, mock_get_ticker):
        mock_get_ticker.return_value = self.__mock_ticker()
        orders = self.__mock_orders('OMG')

        gain = get_gain_for_currency(orders, 'OMG')

        self.assertEqual(100, gain)

    @patch("dashboard_data.get_ticker")
    @patch("dashboard_data.eth_to_btc")
    def test_get_gain_for_eth_exchange(self, mock_eth_to_btc, mock_get_ticker):
        mock_eth_to_btc.return_value = 0.00032
        mock_get_ticker.return_value = self.__mock_ticker()
        orders = [{
            'OrderType': 'LIMIT_BUY',
            'Exchange': 'ETH-OMG',
            'Closed': '2017-09-04T07:51:24.79',
            'Quantity': 5.0,
            'Price': 0.015,
            'PricePerUnit': 0.003
        }]

        gain = get_gain_for_currency(orders, 'OMG')

        self.assertEqual(-94.375, gain)

    @patch("dashboard_data.get_ticker")
    def test_get_gain_for_currency_with_sells(self, mock_get_ticker):
        mock_get_ticker.return_value = self.__mock_ticker()
        test_exchange = 'BTC-OMG'
        order_buy_1 = {
            'OrderType': 'LIMIT_BUY',
            'Exchange': test_exchange,
            'Quantity': 5.0,
            'PricePerUnit': 0.003
        }
        order_sell =  {
            'OrderType': 'LIMIT_SELL',
            'Exchange': test_exchange,
            'Quantity': 3
        }
        order_buy_2 = {
            'OrderType': 'LIMIT_BUY',
            'Exchange': test_exchange,
            'Quantity': 4.0,
            'PricePerUnit': 0.075
        }
        orders = [order_buy_1, order_sell, order_buy_2]

        gain = get_gain_for_currency(orders, 'OMG')

        self.assertEqual(-28, gain)

    def __mock_ticker(self):
        return {'Ask': 0.006, 'Bid': 0.003, 'Last': 0.006}

    def __mock_orders(self, currency):
        exchange = 'BTC-%s' % currency
        order_1 = {
            'OrderType': 'LIMIT_BUY',
            'Exchange': exchange,
            'Quantity': 5.0,
            'PricePerUnit': 0.003
        }

        return [order_1]

