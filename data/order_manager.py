from api.market_api import put_sell_limit
from api.account_api import get_balance
from api.market_api import get_opened_orders, cancel_order
from helpers.market_helpers import extract_currency
from helpers.order_utilities import only_sells


def cancel_all_opened_sell_orders(market):
    all_opened_orders = get_opened_orders(market)
    only_sell_orders = only_sells(all_opened_orders)
    opened_orders_uuids = list(map(lambda order: order['OrderUuid'], only_sell_orders))
    for uuid in opened_orders_uuids:
        cancel_order(uuid)


def sell_all_limit(market, rate):
    balance = get_balance(extract_currency(market))['Available']

    return put_sell_limit(market, balance, rate)
