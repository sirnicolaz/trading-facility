import copy
from api.price_api import eth_to_btc, btc_to_eth

__PRECISION = 15


def __convert_to_btc(order):
    one_eth_value = eth_to_btc(order['Closed'])
    order['PricePerUnit'] = round(float(order['PricePerUnit']) * float(one_eth_value),__PRECISION)
    order['Price'] = round(float(order['Price']) * float(one_eth_value), __PRECISION)
    order['Exchange'] = order['Exchange'].replace("ETH-", "BTC-")


def to_btc(orders):
    copy_orders = copy.deepcopy(orders)
    for order in copy_orders:
        exchange = order['Exchange']
        if "ETH-" in exchange:
            __convert_to_btc(order)

    return copy_orders


def to_eth(orders):
    copy_orders = copy.deepcopy(orders)
    for order in copy_orders:
        exchange = order['Exchange']
        if "ETH-" in exchange:
            __convert_to_btc(order)

    return copy_orders