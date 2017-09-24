import urllib.request
from urllib.request import Request, urlopen
import json
from uuid import uuid1
import hmac
from lxml import html
from multiprocessing import Pipe

_PIPE_PARENT, _PIPE_CHILD = Pipe()
QUEUE = None

def set_queue(queue):
    global QUEUE
    QUEUE = queue


def get(url):
    response = urllib.request.urlopen(url)
    encoding = response.info().get_content_charset('utf8')
    data = json.loads(response.read().decode(encoding))

    return data


def get_verification_token():
    url = 'https://bittrex.com/Market/Index?MarketName=BTC-PAY'
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    response_pipe = _PIPE_CHILD
    QUEUE.put({
        "url": url,
        "accept": accept,
        "response_pipe": response_pipe
    })

    response = _PIPE_PARENT.recv()

    content = response.decode("utf-8")
    tree = html.fromstring(content)

    token = tree.xpath('//input[@name="__RequestVerificationToken"]')[0].value

    return token


def put_sell_order(query):
    url = 'https://bittrex.com/api/v2.0/auth/market/TradeSell'
    accept = 'application/json, text/javascript, */*; q=0.01'
    response_pipe = _PIPE_CHILD
    auth_query = query + "&__RequestVerificationToken=%s" % get_verification_token()

    #q.add_header('X-Requested-With', 'XMLHttpRequest')
    #q.data = b'MarketName=BTC-PAY&OrderType=LIMIT&Quantity=10.00000000&Rate=0.00006000&TimeInEffect=GOOD_TIL_CANCELLED&ConditionType=LESS_THAN&Target=0.00006000&__RequestVerificationToken=lfgsZhphOV9hGDiz1AzR60MPGBY8accgOg-PyAqVrJTcIIwz0KqQJId5hZ2opJ9bJXDsH8FA3txkWzKjeG3RozS1fRulab2DaMv5aOArXSEF8eZ9mWBRs1s7DboJ5YAbUPJZSA2'

    QUEUE.put({
        'url': url,
        'accept': accept,
        'response_pipe': response_pipe,
        'query': auth_query
    })
    response = _PIPE_PARENT.recv()

    data = json.loads(response.decode('utf-8'))

    return data


def get_auth(url, api_key, api_secret):
    if not api_secret or not api_key:
        raise ValueError("Missing API Key and/or API Secret")

    auth_url = __authenticate_url(url, api_key)
    sign = hmac.new(str.encode(api_secret), str.encode(auth_url), digestmod="sha512").hexdigest()

    q = Request(auth_url)
    q.add_header('apisign', sign)
    response = urlopen(q)

    encoding = response.info().get_content_charset('utf8')
    data = json.loads(response.read().decode(encoding))

    return data


def __authenticate_url(url, api_key):
    nonce = str(uuid1())
    api_key_param = "apikey=%s&nonce=%s" % (api_key, nonce)
    if '?' not in url:
        return url + "?" + api_key_param
    else:
        return url + "&" + api_key_param