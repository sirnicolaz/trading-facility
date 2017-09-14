from copy import deepcopy


def filter_currency(orders, currency):
    return list(filter(lambda order: currency.upper() in order["Exchange"], orders))


def filter_sells(orders):
    return list(filter(lambda order: order['OrderType'] == 'LIMIT_SELL', deepcopy(orders)))


def filter_buys(orders):
    return list(filter(lambda order: order['OrderType'] == 'LIMIT_BUY', deepcopy(orders)))

