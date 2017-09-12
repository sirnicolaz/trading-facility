from api.market_api import put_sell_limit
from api.account_api import get_balance
from api.market_api import get_opened_orders, cancel_order
from helpers.market_helpers import extract_currency


def cancel_all_opened_orders(market):
    opened_orders_uuids = list(map(lambda order: order['OrderUuid'], get_opened_orders(market)))
    for uuid in opened_orders_uuids:
        cancel_order(uuid)


def sell_all_limit(market, rate):
    balance = get_balance(extract_currency(market))['Available']

    return put_sell_limit(market, balance, rate)
