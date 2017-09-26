from unittest import TestCase
from unittest.mock import patch

from controllers.order_maker import cancel_all_opened_sell_orders, sell_all_limit, force_put_sell_all_limit_order, \
    force_put_conditional_sell_all_order


class TestOrderMaker(TestCase):
    @patch("controllers.order_maker.get_balance")
    @patch("controllers.order_maker.put_sell_limit")
    def test_sell_all_limit(self, mock_put_sell_limit, mock_get_balance):
        mock_get_balance.return_value = {'Available': 42}
        mock_put_sell_limit.return_value = 'test'

        result = sell_all_limit("BTC-DIO", 0.1)

        mock_get_balance.assert_called_with("DIO")
        mock_put_sell_limit.assert_called_with("BTC-DIO", 42, 0.1)
        self.assertEqual(result, 'test')

    @patch("controllers.order_maker.get_opened_orders")
    @patch("controllers.order_maker.cancel_order")
    def test_cancel_all_opened_orders_fetches_right_orders(self, mock_cancel_order, mock_get_opened_orders):
        cancel_all_opened_sell_orders("BTC-DIO")

        mock_get_opened_orders.assert_called_with("BTC-DIO")

    @patch("controllers.order_maker.get_opened_orders")
    @patch("controllers.order_maker.cancel_order")
    def test_cancel_all_opened_orders_only_sell_orders(self, mock_cancel_order, mock_get_opened_orders):
        mock_get_opened_orders.return_value = [{"OrderUuid": 42, "OrderType": "LIMIT_SELL"},
                                               {"OrderUuid": 43, "OrderType": "LIMIT_BUY"}]

        cancel_all_opened_sell_orders("BTC-DIO")

        mock_cancel_order.assert_any_call(42)

    @patch("controllers.order_maker.get_opened_orders")
    @patch("controllers.order_maker.cancel_order")
    def test_cancel_all_opened_orders_with_no_opened_orders(self, mock_cancel_order, mock_get_opened_orders):
        mock_get_opened_orders.return_value = []

        cancel_all_opened_sell_orders("BTC-DIO")

        self.assertEqual(mock_cancel_order.call_count, 0)

    @patch("controllers.order_maker.cancel_all_opened_sell_orders")
    @patch("controllers.order_maker.sell_all_limit")
    def test_put_sell_limit_order_cancels_then_put(self, mock_sell_all_limit, mock_cancel_all_opened_orders):
        mock_sell_all_limit.return_value = "test"
        test_market = "BTC-DIO"
        test_rate = 42

        result = force_put_sell_all_limit_order(test_market, rate=test_rate)

        mock_cancel_all_opened_orders.assert_called_with(test_market)
        mock_sell_all_limit.assert_called_with(test_market, test_rate)
        self.assertEquals("test", result)

    @patch("controllers.order_maker.cancel_all_opened_sell_orders")
    @patch("controllers.order_maker.put_conditional_sell_limit")
    @patch("controllers.order_maker.is_alive")
    @patch("controllers.order_maker.get_balance")
    def test_force_put_conditional_sell_all_order_alive(self, mock_get_balance, mock_is_alive,
                                                        mock_put_conditional_sell_limit, mock_cancel_all_opened_orders):
        mock_is_alive.return_value = True
        mock_get_balance.return_value = {'Available': 0.5}
        mock_put_conditional_sell_limit.return_value = "test result"

        result = force_put_conditional_sell_all_order("BTC-EUR", "0.3")

        self.assertTrue(mock_cancel_all_opened_orders.called)
        self.assertEquals("test result", result)

    @patch("controllers.order_maker.cancel_all_opened_sell_orders")
    @patch("controllers.order_maker.put_conditional_sell_limit")
    @patch("controllers.order_maker.is_alive")
    @patch("controllers.order_maker.get_balance")
    def test_force_put_conditional_sell_all_order_not_alive(self, mock_get_balance, mock_is_alive,
                                                        mock_put_conditional_sell_limit, mock_cancel_all_opened_orders):
        mock_is_alive.return_value = False

        with self.assertRaises(ConnectionError) as _:
            force_put_conditional_sell_all_order("any", "any")

    @patch("controllers.order_maker.cancel_all_opened_sell_orders")
    @patch("controllers.order_maker.put_conditional_sell_limit")
    @patch("controllers.order_maker.is_alive")
    @patch("controllers.order_maker.get_balance")
    def test_force_put_conditional_sell_all_order_truncated_values(self, mock_get_balance, mock_is_alive,
                                                                   mock_put_conditional_sell_limit,
                                                                   mock_cancel_all_opened_orders):
        mock_is_alive.return_value = True
        mock_get_balance.return_value = {'Available': "0.54928749238472938472983"}
        test_rate = "0.1283761287361283761"

        force_put_conditional_sell_all_order("BTC-EUR", test_rate)

        expected_rate = "0.128376128736128"
        expected_balance = "0.549287492384729"
        mock_put_conditional_sell_limit.assert_called_with("BTC-EUR",
                                                           expected_balance, rate=expected_rate, target=expected_rate)

    @patch("controllers.order_maker.cancel_all_opened_sell_orders")
    @patch("controllers.order_maker.put_conditional_sell_limit")
    @patch("controllers.order_maker.is_alive")
    @patch("controllers.order_maker.get_balance")
    def test_force_put_conditional_sell_all_order_cancel_and_sell(self, mock_get_balance, mock_is_alive,
                                                                  mock_put_conditional_sell_limit,
                                                                  mock_cancel_all_opened_orders):
        mock_is_alive.return_value = True
        mock_get_balance.return_value = {'Available': "0.54928749238472938472983"}

        force_put_conditional_sell_all_order("BTC-EUR", "0.42")

        self.assertTrue(mock_cancel_all_opened_orders.called)
        self.assertTrue(mock_put_conditional_sell_limit.called)

    @patch("controllers.order_maker.cancel_all_opened_sell_orders")
    @patch("controllers.order_maker.put_conditional_sell_limit")
    @patch("controllers.order_maker.is_alive")
    @patch("controllers.order_maker.get_balance")
    def test_force_put_conditional_sell_all_order_cancel_right_market(self, mock_get_balance, mock_is_alive,
                                                                   _, mock_cancel_all_opened_orders):
        mock_is_alive.return_value = True
        mock_get_balance.return_value = {'Available': "0.54928749238472938472983"}
        test_market = "BTC-EUR"
        force_put_conditional_sell_all_order(test_market, "0.42")

        mock_cancel_all_opened_orders.assert_called_with(test_market)

