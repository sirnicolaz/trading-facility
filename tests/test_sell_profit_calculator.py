from unittest import TestCase
from data.sell_profit_calculator import get_sell_profit


class TestSellProfitCalculator(TestCase):
    def test_get_sell_profit_base_case(self):
        orders = [{
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.003
        }, {
            'OrderType': 'LIMIT_SELL',
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.006
        }]

        result = get_sell_profit(orders)

        expected_result = 0.003 * 5
        self.assertEqual(expected_result, result)

    def test_get_sell_profit_multiple_buys(self):
        orders = [{
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 3.0,
            'PricePerUnit': 0.003
        }, {
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 2.0,
            'PricePerUnit': 0.003
        }, {
            'OrderType': 'LIMIT_SELL',
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.006
        }]

        result = get_sell_profit(orders)

        expected_result = 0.003 * 5
        self.assertEqual(expected_result, result)

    def test_get_sell_profit_multiple_buys_different_rates(self):
        orders = [{
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 3.0,
            'PricePerUnit': 0.003
        }, {
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 2.0,
            'PricePerUnit': 0.006
        }, {
            'OrderType': 'LIMIT_SELL',
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.006
        }]

        result = get_sell_profit(orders)

        expected_result = 0.009
        self.assertEqual(expected_result, result)

    def test_get_sell_profit_multiple_sells(self):
        orders = [{
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.003
        }, {
            'OrderType': 'LIMIT_SELL',
            'ActualQuantity': 2.0,
            'PricePerUnit': 0.006
        }, {
            'OrderType': 'LIMIT_SELL',
            'ActualQuantity': 3.0,
            'PricePerUnit': 0.006
        }]

        result = get_sell_profit(orders)

        expected_result = 0.003 * 5
        self.assertEqual(expected_result, result)

    def test_get_sell_profit_multiple_sells_different_rates(self):
        orders = [{
            'OrderType': 'LIMIT_BUY',
            'ActualQuantity': 5.0,
            'PricePerUnit': 0.003
        }, {
            'OrderType': 'LIMIT_SELL',
            'ActualQuantity': 2.0,
            'PricePerUnit': 0.003
        }, {
            'OrderType': 'LIMIT_SELL',
            'ActualQuantity': 3.0,
            'PricePerUnit': 0.006
        }]

        result = get_sell_profit(orders)

        expected_result = 0.009
        self.assertEqual(expected_result, result)