from unittest import TestCase
from unittest.mock import patch

from data.order_manager import cancel_all_opened_orders, sell_all_limit


class TestOrderManager(TestCase):
    @patch("data.order_manager.get_balance")
    @patch("data.order_manager.put_sell_limit")
    def test_sell_all_limit(self, mock_put_sell_limit, mock_get_balance):
        mock_get_balance.return_value = {'Available': 42}
        mock_put_sell_limit.return_value = 'test'

        result = sell_all_limit("BTC-DIO", 0.1)

        mock_get_balance.assert_called_with("DIO")
        mock_put_sell_limit.assert_called_with("BTC-DIO", 42, 0.1)
        self.assertEqual(result, 'test')

    @patch("data.order_manager.get_opened_orders")
    @patch("data.order_manager.cancel_order")
    def test_cancel_all_opened_orders_fetches_right_orders(self, mock_cancel_order, mock_get_opened_orders):
        cancel_all_opened_orders("BTC-DIO")

        mock_get_opened_orders.assert_called_with("BTC-DIO")

    @patch("data.order_manager.get_opened_orders")
    @patch("data.order_manager.cancel_order")
    def test_cancel_all_opened_orders(self, mock_cancel_order, mock_get_opened_orders):
        mock_get_opened_orders.return_value = [{"OrderUuid": 42}, {"OrderUuid": 43}]

        cancel_all_opened_orders("BTC-DIO")

        mock_cancel_order.assert_any_call(42)
        mock_cancel_order.assert_any_call(43)

    @patch("data.order_manager.get_opened_orders")
    @patch("data.order_manager.cancel_order")
    def test_cancel_all_opened_orders_with_no_opened_orders(self, mock_cancel_order, mock_get_opened_orders):
        mock_get_opened_orders.return_value = []

        cancel_all_opened_orders("BTC-DIO")

        self.assertEqual(mock_cancel_order.call_count, 0)

