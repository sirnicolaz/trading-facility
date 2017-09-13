from environment import API_KEY, API_SECRET, ORDER_HISTORY_FILE
from functools import lru_cache
from api.endpoints.bittrex_endpoints import AccountEndpoints
from api.request_handler import get_auth


def __fetch(url):
    return get_auth(url, API_KEY, API_SECRET)['result']


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

