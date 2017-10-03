from api.endpoints.bittrex_endpoints import PrivateMarketEndpoints
from api.request_handler import get


def __fetch(url):
    return get(url)


def put_conditional_sell_limit(market, quantity, rate, target):
    return __fetch(PrivateMarketEndpoints.put_conditional_sell(market, quantity=quantity, rate=rate, target=target))


def is_alive():
    return __fetch(PrivateMarketEndpoints.is_alive())