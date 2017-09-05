from copy import deepcopy


def only_sells(orders):
    return list(filter(lambda order: order['OrderType'] == 'LIMIT_SELL', deepcopy(orders)))


def only_buys(orders):
    return list(filter(lambda order: order['OrderType'] == 'LIMIT_BUY', deepcopy(orders)))