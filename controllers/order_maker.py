from api.account_api import get_balance
from api.market_api import get_opened_orders, cancel_order, put_sell_limit
from api.private_market_api import put_conditional_sell_limit, is_alive
from utilities.market_helpers import extract_currency
from utilities.order_filters import filter_sells


def __get_percentage_from_balance(market, percentage=100.0):
    balance = get_balance(extract_currency(market))['Balance']
    amount = float(balance) / 100.0 * percentage

    return amount


def cancel_all_opened_sell_orders(market):
    all_opened_orders = get_opened_orders(market)
    only_sell_orders = filter_sells(all_opened_orders)
    opened_orders_uuids = list(map(lambda order: order['OrderUuid'], only_sell_orders))
    for uuid in opened_orders_uuids:
        cancel_order(uuid)


def sell_all_limit(market, rate, percentage_amount=100.0):
    balance = __get_percentage_from_balance(market=market, percentage=percentage_amount)

    return put_sell_limit(market, balance, rate)


def force_put_sell_all_limit_order(market, rate, percentage_amount=100.0):
    cancel_all_opened_sell_orders(market)
    return sell_all_limit(market, rate, percentage_amount)


def force_put_conditional_sell_all_order(market, rate, percentage_amount=100.0):
    if is_alive():
        balance_to_sell = __get_percentage_from_balance(market=market, percentage=percentage_amount)
        truncated_balance = "%.15f" % float(balance_to_sell)
        truncated_rate = "%.15f" % float(rate)

        cancel_all_opened_sell_orders(market)
        return put_conditional_sell_limit(market, truncated_balance, rate=truncated_rate, target=truncated_rate)
    else:
        raise ConnectionError("Private api looks dead. Refresh the cookies.")

