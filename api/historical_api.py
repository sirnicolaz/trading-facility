from api.endpoints.cryptocompare_endpoints import HistoricalEndpoints
from api.request_handler import get


def __fetch(url):
    return get(url)['Data']


def get_historical_hour(from_currency, to_currency, limit=100):
    url = HistoricalEndpoints.get_history_hour(from_currency, to_currency, limit)

    return __fetch(url)

