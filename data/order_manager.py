from environment import ORDER_HISTORY_FILE
from api.market_api import put_sell_limit
from api.account_api import get_balance, get_order_history
from api.market_api import get_opened_orders, cancel_order
from helpers.market_helpers import extract_currency
from helpers.order_filters import filter_sells
from _datetime import datetime
import csv


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


def cancel_all_opened_sell_orders(market):
    all_opened_orders = get_opened_orders(market)
    only_sell_orders = filter_sells(all_opened_orders)
    opened_orders_uuids = list(map(lambda order: order['OrderUuid'], only_sell_orders))
    for uuid in opened_orders_uuids:
        cancel_order(uuid)


def sell_all_limit(market, rate):
    balance = get_balance(extract_currency(market))['Available']

    return put_sell_limit(market, balance, rate)


def put_sell_all_limit_order(market, rate):
    cancel_all_opened_sell_orders(market)
    return sell_all_limit(market, rate)

