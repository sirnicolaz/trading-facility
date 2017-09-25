import json
from lxml import html
from multiprocessing import Pipe


_PIPE_PARENT, _PIPE_CHILD = Pipe()
QUEUE = None


def set_queue(queue):
    global QUEUE
    QUEUE = queue


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


def is_alive():
    url = 'https://bittrex.com/Market/Index?MarketName=BTC-PAY'
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    response_pipe = _PIPE_CHILD

    QUEUE.put({
        "url": url,
        "accept": accept,
        "response_pipe": response_pipe
    })

    response = _PIPE_PARENT.recv()

    return response is not None


def put_sell_order(query):
    url = 'https://bittrex.com/api/v2.0/auth/market/TradeSell'
    accept = 'application/json, text/javascript, */*; q=0.01'
    response_pipe = _PIPE_CHILD
    auth_query = query + "&__RequestVerificationToken=%s" % get_verification_token()

    QUEUE.put({
        'url': url,
        'accept': accept,
        'response_pipe': response_pipe,
        'query': auth_query
    })
    response = _PIPE_PARENT.recv()

    data = json.loads(response.decode('utf-8'))

    return data