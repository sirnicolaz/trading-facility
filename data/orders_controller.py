import copy
import csv
from datetime import datetime

from api.account_api import get_order_history
from environment import REFERENCE_CURRENCY, ORDER_HISTORY_FILE
from functools import reduce
from itertools import groupby
from data.conversion_manager import convert_orders_to_btc, convert_orders_to_eth
from utilities.order_filters import filter_buys, filter_sells


def __generate_history_entry(row):
    return {
        "OrderUuid": row[0],
        "Exchange": row[1],
        "Closed": datetime.strptime(row[8], '%m/%d/%Y %H:%M:%S %p').strftime('%Y-%m-%dT%H:%M:%S.%f'),
        "Opened": datetime.strptime(row[7], '%m/%d/%Y %H:%M:%S %p').strftime('%Y-%m-%dT%H:%M:%S.%f'),
        "OrderType": row[2],
        "Quantity": float(row[3]),
        "QuantityRemaining": 0,
        "PricePerUnit": float(row[4]),
        "Price": float(row[6])
    }


def __subtract_sells_from_buys(sells, buys):
    new_buys = copy.deepcopy(buys)
    sum_sells = reduce(lambda tot, sell: tot + sell['ActualQuantity'], sells, 0)
    for buy in reversed(new_buys):
        if sum_sells <= 0:
            break

        sum_sells -= buy['ActualQuantity']
        buy['ActualQuantity'] = abs(min(round(sum_sells, 12), 0))

    return new_buys


def __consolidate_orders(orders):
    if REFERENCE_CURRENCY == "btc":
        orders = convert_orders_to_btc(orders)
    elif REFERENCE_CURRENCY == "eth":
        orders = convert_orders_to_eth(orders)

    extended_orders = __with_actual_quantities(orders)

    return extended_orders


def __with_actual_quantities(orders):
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


# For each market, it subtracts the sells from the buys (in chronological order).
# This is useful when one needs to know only the currently available units,
# associated to their value when bought. For example:
# [Buy 5 @0.5, Sell 2 @0.2, Buy 3 @0.1] -> [Buy 3 @0.5, Buy 3 @0.1]
# From the initial 5 units @0.5 value, only 3 are left (because 2 were sold in the meantime)
def remove_sells_from_buys(orders):
    processed_orders = []
    sorted_by_exchange = sorted(orders, key=lambda x: x["Exchange"])
    for market, group in groupby(sorted_by_exchange, lambda item: item["Exchange"]):
        currency_orders = list(group)
        currency_sells = filter_sells(currency_orders)
        currency_buys = filter_buys(currency_orders)

        processed_orders += __subtract_sells_from_buys(currency_sells, currency_buys)

    return processed_orders


# Consolidation mean:
# - all orders converted to reference currency
# - adds actual quantity fulfilled for each order
def consolidated_user_orders():
    orders = load_order_history()
    return __consolidate_orders(orders)


# It uses both local orders and remote history (Bittrex only keeps last month of orders,
# so they need to be enriched with local data)
def load_order_history():
    orders = []
    if ORDER_HISTORY_FILE is not None:
        csv_file = open(ORDER_HISTORY_FILE)
        content = csv.reader(csv_file)
        rows = [row for row in content][1:]
        orders = [__generate_history_entry(row) for row in rows]

    recent_orders = get_order_history()
    existing_uuids = list(map(lambda order: order['OrderUuid'], orders))
    for order in recent_orders:
        if order['OrderUuid'] not in existing_uuids:
            orders += [order]

    return orders
