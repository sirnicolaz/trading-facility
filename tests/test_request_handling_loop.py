import threading
from multiprocessing import Queue, Pipe
from unittest import TestCase
from unittest.mock import patch

from api.hidden_api_manager import request_handling_loop


class TestHiddenAPIManager(TestCase):
    @patch("api.hidden_api_manager.__COOKIES_FILE", "resources/cookies.txt")
    def test_request_handling_loop(self):
        queue = Queue()
        parent, child = Pipe()
        thread = threading.Thread(target=request_handling_loop, args=(queue,))
        thread.daemon = True  # Daemonize thread
        thread.start()

        url = 'https://bittrex.com/Market/Index?MarketName=BTC-PAY'
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'

        queue.put({
            'url': url,
            'accept': accept,
            'response_pipe': child
        })

        if parent.poll(timeout=3):
            result = parent.recv()
            self.assertIsNotNone(result)
        else:
            self.fail()
