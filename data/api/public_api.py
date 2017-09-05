from data.api.endpoints import PublicEndpoints
from data.api.request_handler import get


def __fetch(url):
    return get(url)['result']


def get_markets():
    return __fetch(PublicEndpoints.get_markets())


def get_currencies():
    return __fetch(PublicEndpoints.get_currencies())


def get_ticker(market):
    return __fetch(PublicEndpoints.get_ticker(market))