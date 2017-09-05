import copy
from datetime import datetime
from functools import lru_cache
from data.api.request_handler import get

__PRECISION = 15


# string format: '2017-09-04T07:51:24.79'
@lru_cache(maxsize=None)
def eth_to_btc(time_string):
    dt = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S.%f')
    timestamp = int(dt.timestamp())
    result = get("https://min-api.cryptocompare.com/data/pricehistorical?fsym=ETH&tsyms=BTC&ts=%s&extraParams=your_app_name"
        % timestamp)

    return result['ETH']['BTC']


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
