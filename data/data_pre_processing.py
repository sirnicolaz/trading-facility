import copy
from functools import reduce


def repair_quantities(orders):
    copy_orders = copy.deepcopy(orders)
    for order in copy_orders:
        # A bug on bittrex apis returns quantity 0 sometimes
        if float(order['Quantity']) <= 0:
            order['Quantity'] = float(order['Price']) / float(order['PricePerUnit'])

        if float(order['QuantityRemaining']) > 0:
            order['Quantity'] = float(order['Quantity']) - float(order['QuantityRemaining'])

    return copy_orders


def subtract_sells_from_buys(sells, buys):
    new_buys = copy.deepcopy(buys)
    sum_sells = reduce(lambda tot, sell: tot + sell['Quantity'], sells, 0)
    for buy in reversed(new_buys):
        sum_sells -= buy['Quantity']
        buy['Quantity'] = abs(min(round(sum_sells, 12), 0))

        if sum_sells <= 0:
            break

    return new_buys
