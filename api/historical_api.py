from cachetools.func import ttl_cache
from api.endpoints.cryptocompare_endpoints import HistoricalEndpoints
from api.request_handler import get


def __fetch(url):
    return get(url)['Data']


@ttl_cache(maxsize=4000, ttl=60)
def get_historical_hour(from_currency, to_currency, limit=100, aggregate=1):
    url = HistoricalEndpoints.get_history_hour(from_currency, to_currency, limit, aggregate)

    return __fetch(url)
