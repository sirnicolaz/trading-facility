import json
from lxml import html
from multiprocessing import Pipe

QUEUE = None


def set_queue(queue):
    global QUEUE
    QUEUE = queue


def __get_verification_token():
    url = 'https://bittrex.com/Market/Index?MarketName=BTC-PAY'
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    response_pipe_parent, response_pipe_child = Pipe()
    QUEUE.put({
        "url": url,
        "accept": accept,
        "response_pipe": response_pipe_child
    })

    response = response_pipe_parent.recv()

    content = response.decode("utf-8")
    tree = html.fromstring(content)

    verification_token_node = tree.xpath('//input[@name="__RequestVerificationToken"]')
    if len(verification_token_node) > 0:
        token = verification_token_node[0].value
    else:
        token = None

    return token


def is_alive():
    token = __get_verification_token()

    return token is not None


def put_sell_order(query):
    url = 'https://bittrex.com/api/v2.0/auth/market/TradeSell'
    return _perform_query(url, query)


def _perform_query(url, query=None):
    accept = 'application/json, text/javascript, */*; q=0.01'
    response_pipe_parent, response_pipe_child = Pipe()
    auth_query = "__RequestVerificationToken=%s" % __get_verification_token()

    if query is not None:
        auth_query = query + "&" + auth_query


    QUEUE.put({
        'url': url,
        'accept': accept,
        'response_pipe': response_pipe_child,
        'query': auth_query
    })
    response = response_pipe_parent.recv()

    data = json.loads(response.decode('utf-8'))

    return data


def put_conditional_sell_limit(market, quantity, rate, target):
    query = 'MarketName=%s&OrderType=LIMIT&Quantity=%s&Rate=%s&TimeInEffect=GOOD_TIL_CANCELLED&' \
            'ConditionType=LESS_THAN&Target=%s' % (market, quantity, rate, target)

    return put_sell_order(query)
