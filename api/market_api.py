from environment import API_SECRET, API_KEY
from api.endpoints.bittrex_endpoints import MarketEndpoints
from api.request_handler import get_auth


def __fetch(url):
    return get_auth(url, API_KEY, API_SECRET)['result']


def put_sell_limit(market, quantity, rate):
    return __fetch(MarketEndpoints.put_sell_limit(market, quantity=quantity, rate=rate))


def cancel_order(uuid):
    return __fetch(MarketEndpoints.cancel_order(uuid))


def get_opened_orders(market):
    return __fetch(MarketEndpoints.get_opened_orders(market))