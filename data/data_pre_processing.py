import copy
from functools import reduce
from itertools import groupby

from api.account_api import get_order_history
from data.conversion_manager import convert_orders_to_btc, convert_orders_to_eth
from helpers.order_filters import filter_buys, filter_sells


def __subtract_sells_from_buys(sells, buys):
    new_buys = copy.deepcopy(buys)
    sum_sells = reduce(lambda tot, sell: tot + sell['ActualQuantity'], sells, 0)
    for buy in reversed(new_buys):
        if sum_sells <= 0:
            break

        sum_sells -= buy['ActualQuantity']
        buy['ActualQuantity'] = abs(min(round(sum_sells, 12), 0))


    return new_buys


def __simplify_orders(reference_currency, orders):
    if reference_currency == "btc":
        orders = convert_orders_to_btc(orders)
    elif reference_currency == "eth":
        orders = convert_orders_to_eth(orders)

    extended_orders = with_actual_quantities(orders)

    return extended_orders


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
        currency_sells = filter_sells(currency_orders)
        currency_buys = filter_buys(currency_orders)

        processed_orders += __subtract_sells_from_buys(currency_sells, currency_buys)

    return processed_orders


def simplified_user_orders(reference_currency="btc"):
    orders = get_order_history()

    return __simplify_orders(reference_currency.lower(), orders)