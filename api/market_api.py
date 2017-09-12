import os

from api.endpoints.bittrex_endpoints import MarketEndpoints
from api.request_handler import get_auth, put_sell_order

api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')



def __fetch(url):
    return get_auth(url, api_key, api_secret)['result']


def put_sell_limit(market, quantity, rate):
    return __fetch(MarketEndpoints.put_sell_limit(market, quantity=quantity, rate=rate))


def put_conditional_sell_limit(market, quantity, rate, target):
    query = 'MarketName=%s&OrderType=LIMIT&Quantity=%s&Rate=%s&TimeInEffect=GOOD_TIL_CANCELLED&' \
            'ConditionType=LESS_THAN&Target=%s' % (market, quantity, rate, target)

    return put_sell_order(query)


def cancel_order(uuid):
    return __fetch(MarketEndpoints.cancel_order(uuid))


def get_opened_orders(market):
    return __fetch(MarketEndpoints.get_opened_orders(market))