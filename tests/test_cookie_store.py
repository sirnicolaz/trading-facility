from unittest import TestCase
from unittest.mock import patch

from bittrex_proxy.utilities.cookie_store import get_private_api_cookie, update_private_api_cookie
from tests.helpers import cookie_helper


class TestCookieStore(TestCase):
    @patch("bittrex_proxy.utilities.cookie_store.COOKIES_FILE", cookie_helper.MOCK_COOKIES_PATH)
    def test_update_private_api_cookie_case1(self):
        set_cookie_header = ".AspNet.ApplicationCookie=newValue123; othercookie=value"
        cookie_helper.store_mock_cookie("akey=avalue; .AspNet.ApplicationCookie=oldvalue; othervalues")

        update_private_api_cookie(set_cookie_header)

        result = cookie_helper.get_mock_cookie()

        self.assertEqual(result, "akey=avalue; othervalues;.AspNet.ApplicationCookie=newValue123")

    @patch("bittrex_proxy.utilities.cookie_store.COOKIES_FILE", cookie_helper.MOCK_COOKIES_PATH)
    def test_update_private_api_cookie_case2(self):
        set_cookie_header = "key=value;.AspNet.ApplicationCookie=newValue123"
        cookie_helper.store_mock_cookie("akey=avalue; .AspNet.ApplicationCookie=oldvalue; othervalues")

        update_private_api_cookie(set_cookie_header)

        result = cookie_helper.get_mock_cookie()

        self.assertEqual(result, "akey=avalue; othervalues;.AspNet.ApplicationCookie=newValue123")

    @patch("bittrex_proxy.utilities.cookie_store.COOKIES_FILE", cookie_helper.MOCK_COOKIES_PATH)
    def test_update_private_api_cookie_case3(self):
        set_cookie_header = "key=value;.AspNet.ApplicationCookie=newValue123"
        cookie_helper.store_mock_cookie("akey=avalue; .AspNet.ApplicationCookie=oldvalue")

        update_private_api_cookie(set_cookie_header)

        result = cookie_helper.get_mock_cookie()

        self.assertEqual(result, "akey=avalue;.AspNet.ApplicationCookie=newValue123")

    @patch("bittrex_proxy.utilities.cookie_store.COOKIES_FILE", cookie_helper.MOCK_COOKIES_PATH)
    def test_update_private_api_cookie_case4(self):
        set_cookie_header = ".AspNet.ApplicationCookie=newValue123"
        cookie_helper.store_mock_cookie("akey=avalue; .AspNet.ApplicationCookie=oldvalue")

        update_private_api_cookie(set_cookie_header)

        result = cookie_helper.get_mock_cookie()

        self.assertEqual(result, "akey=avalue;.AspNet.ApplicationCookie=newValue123")

    @patch("bittrex_proxy.utilities.cookie_store.COOKIES_FILE", cookie_helper.MOCK_COOKIES_PATH)
    def test_update_private_api_cookie_no_cookie(self):
        set_cookie_header = "key=value"
        cookie_helper.store_mock_cookie("akey=avalue; .AspNet.ApplicationCookie=oldvalue")

        with self.assertRaises(ValueError) as context:
            update_private_api_cookie(set_cookie_header)

    @patch("bittrex_proxy.utilities.cookie_store.COOKIES_FILE", cookie_helper.MOCK_COOKIES_PATH)
    def test_get_private_api_cookie(self):
        cookie_helper.store_mock_cookie("akey=avalue; anotherkey=anothervalue\n")

        result = get_private_api_cookie()

        self.assertEqual(result, "akey=avalue; anotherkey=anothervalue")