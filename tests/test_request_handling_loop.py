import threading
from multiprocessing import Queue, Pipe
from unittest import TestCase
from unittest.mock import patch, MagicMock

from api.hidden_api_manager import request_handling_loop


class TestHiddenAPIManager(TestCase):
    @patch("api.hidden_api_manager.__COOKIES_FILE", "resources/cookies.txt")
    @patch("api.hidden_api_manager.Request")
    @patch("api.hidden_api_manager.urlopen")
    def test_request_handling_loop(self, mock_urlopen, mock_Request):
        mock_response = MagicMock()
        mock_response.read.return_value = "some html"
        mock_response.headers = {'Set-Cookie': 'other cookie'}
        mock_urlopen.return_value = mock_response
        mock_request_instance = MagicMock()
        mock_Request.return_value = mock_request_instance

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
            mock_Request.assert_called_with(url)
            mock_request_instance.add_header.assert_any_call('Cookie', "some cookie")
            mock_request_instance.add_header.assert_any_call('Accept', accept)
        else:
            self.fail()
