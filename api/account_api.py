import os
from functools import lru_cache

from api.endpoints.bittrex_endpoints import AccountEndpoints
from api.request_handler import get_auth

api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')


def __fetch(url):
    return get_auth(url, api_key, api_secret)['result']


@lru_cache(maxsize=None)
def get_balances():
    return __fetch(AccountEndpoints.get_balances())


@lru_cache(maxsize=None)
def get_balance(currency):
    return __fetch(AccountEndpoints.get_balance(currency))


@lru_cache(maxsize=None)
def get_order_history(market=None):
    return __fetch(AccountEndpoints.get_order_history(market))


@lru_cache(maxsize=None)
def get_order(order_uuid):
    return __fetch(AccountEndpoints.get_order(order_uuid))

