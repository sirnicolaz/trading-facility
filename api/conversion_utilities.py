import copy
from datetime import datetime
from functools import lru_cache
from api.endpoints.cryptocompare_endpoints import HistoricalEndpoints
from api.request_handler import get

__PRECISION = 15

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


# string format: '2017-09-04T07:51:24.79'
def eth_to_btc(time_string):
    return get_price("ETH", "BTC", time_string)


def btc_to_eth(time_string):
    return get_price("BTC", "ETH", time_string)


def __convert_to_btc(order):
    one_eth_value = eth_to_btc(order['Closed'])
    order['PricePerUnit'] = round(float(order['PricePerUnit']) * float(one_eth_value),__PRECISION)
    order['Price'] = round(float(order['Price']) * float(one_eth_value), __PRECISION)
    order['Exchange'] = order['Exchange'].replace("ETH-", "BTC-")


def convert_orders_to_btc(orders):
    copy_orders = copy.deepcopy(orders)
    for order in copy_orders:
        exchange = order['Exchange']
        if "ETH-" in exchange:
            __convert_to_btc(order)

    return copy_orders
