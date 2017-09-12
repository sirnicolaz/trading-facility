import threading
from unittest import TestCase
from unittest.mock import patch
from multiprocessing import Pipe
from workers.sell_orders_worker import put_sell_all_limit_order, put_order_loop


class TestSellOrdersWorker(TestCase):

    @patch("workers.sell_orders_worker.cancel_all_opened_sell_orders")
    @patch("workers.sell_orders_worker.sell_all_limit")
    def test_put_sell_limit_order_cancels_then_put(self, mock_sell_all_limit, mock_cancel_all_opened_orders):
        mock_sell_all_limit.return_value = "test"
        test_market = "BTC-DIO"
        test_rate = 42

        result = put_sell_all_limit_order(test_market, rate=test_rate)

        mock_cancel_all_opened_orders.assert_called_with(test_market)
        mock_sell_all_limit.assert_called_with(test_market, test_rate)
        self.assertEquals("test", result)

    @patch("workers.sell_orders_worker.cancel_all_opened_sell_orders")
    @patch("workers.sell_orders_worker.sell_all_limit")
    def test_put_order_loop(self, mock_sell_all_limit, mock_cancel_all_opened_orders):
        test_return_result = {'success': 'true'}
        mock_sell_all_limit.return_value = test_return_result
        test_market = "BTC-DIO"
        test_rate = 42
        test_type = 'limit'

        parent_pipe = self.__start_loop()

        parent_pipe.send({
            'market': test_market,
            'type': test_type,
            'rate': test_rate
        })

        if parent_pipe.poll(timeout=3):
            result = parent_pipe.recv()
            self.assertEqual(result, {'success': True})
            mock_cancel_all_opened_orders.assert_called_with(test_market)
            mock_sell_all_limit.assert_called_with(test_market, test_rate)
        else:
            self.fail()

    def test_put_order_loop_bad_rate(self):
        test_market = "BTC-DIO"
        test_rate = "asd"
        test_type = 'limit'

        parent_pipe = self.__start_loop()

        parent_pipe.send({
            'market': test_market,
            'type': test_type,
            'rate': test_rate
        })

        if parent_pipe.poll(timeout=3):
            result = parent_pipe.recv()
            self.assertEqual(result, {'exception': "could not convert string to float: 'asd'"})
        else:
            self.fail()

    @patch("workers.sell_orders_worker.cancel_all_opened_sell_orders")
    @patch("workers.sell_orders_worker.sell_all_limit")
    def test_put_order_loop_failed_request(self, mock_sell_all_limit, mock_cancel_all_opened_orders):
        test_return_result = {'success': 'false', 'message': 'test message'}
        mock_sell_all_limit.return_value = test_return_result
        test_market = "BTC-DIO"
        test_rate = 42
        test_type = 'limit'

        parent_pipe = self.__start_loop()

        parent_pipe.send({
            'market': test_market,
            'type': test_type,
            'rate': test_rate
        })

        if parent_pipe.poll(timeout=3):
            result = parent_pipe.recv()
            self.assertEqual(result, {'exception': 'test message'})
        else:
            self.fail()

    def test_put_order_loop_unsupported_order(self):
        test_market = "BTC-DIO"
        test_rate = 42
        test_type = 'another'

        parent_pipe = self.__start_loop()

        parent_pipe.send({
            'market': test_market,
            'type': test_type,
            'rate': test_rate
        })

        if parent_pipe.poll(timeout=3):
            result = parent_pipe.recv()
            self.assertEqual(result,  {'exception': 'Only limit orders currently supported'})
        else:
            self.fail()


    def __start_loop(self):
        parent, child = Pipe()
        thread = threading.Thread(target=put_order_loop, args=(child,))
        thread.daemon = True  # Daemonize thread
        thread.start()

        return parent