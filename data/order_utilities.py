from copy import deepcopy


def orders_for_currency(orders, currency):
    return list(filter(lambda order: currency in order["Exchange"], orders))


def only_sells(orders):
    return list(filter(lambda order: order['OrderType'] == 'LIMIT_SELL', deepcopy(orders)))


def only_buys(orders):
    return list(filter(lambda order: order['OrderType'] == 'LIMIT_BUY', deepcopy(orders)))

