from datetime import datetime
from functools import lru_cache
from api.endpoints.cryptocompare_endpoints import HistoricalEndpoints
from api.request_handler import get


# string format: '2017-09-04T07:51:24.79'
@lru_cache(maxsize=None)
def get_price(from_currency, to_currency, time_string=None):
    if time_string:
        dt = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S.%f')
    else:
        dt = datetime.now()

    timestamp = int(dt.timestamp())
    result = get(HistoricalEndpoints.get_price_historical(from_currency, to_currency, timestamp))

    return result[from_currency][to_currency]

