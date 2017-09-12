import copy
from functools import reduce
from itertools import groupby

from api.account_api import get_order_history
from api.conversion_utilities import convert_orders_to_btc
from helpers.order_utilities import only_buys, only_sells


def __subtract_sells_from_buys(sells, buys):
    new_buys = copy.deepcopy(buys)
    sum_sells = reduce(lambda tot, sell: tot + sell['ActualQuantity'], sells, 0)
    for buy in reversed(new_buys):
        if sum_sells <= 0:
            break

        sum_sells -= buy['ActualQuantity']
        buy['ActualQuantity'] = abs(min(round(sum_sells, 12), 0))


    return new_buys


def __simplify_orders(orders):
    btc_orders = convert_orders_to_btc(orders)
    extended_btc_orders = with_actual_quantities(btc_orders)

    return extended_btc_orders


def with_actual_quantities(orders):
    copy_orders = copy.deepcopy(orders)
    actual_quantity_key = 'ActualQuantity'

    for order in copy_orders:
        # A bug on bittrex apis returns quantity 0 sometimes
        if float(order['Quantity']) <= 0:
            order[actual_quantity_key] = float(order['Price']) / float(order['PricePerUnit'])

        if float(order['QuantityRemaining']) > 0:
            order[actual_quantity_key] = float(order['Quantity']) - float(order['QuantityRemaining'])

        if actual_quantity_key not in order:
            order[actual_quantity_key] = order['Quantity']

    return copy_orders


def squash_sells_into_buys(orders):
    processed_orders = []
    sorted_by_exchange = sorted(orders, key=lambda x: x["Exchange"])
    for market, group in groupby(sorted_by_exchange, lambda item: item["Exchange"]):
        currency_orders = list(group)
        currency_sells = only_sells(currency_orders)
        currency_buys = only_buys(currency_orders)

        processed_orders += __subtract_sells_from_buys(currency_sells, currency_buys)

    return processed_orders


def simplified_user_orders():
    orders = get_order_history()

    return __simplify_orders(orders)