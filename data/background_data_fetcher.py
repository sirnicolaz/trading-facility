from itertools import groupby
from time import sleep

from api.conversion_utilities import convert_orders_to_btc
from api.account_api import get_order_history
from data.current_profit_calculator import get_current_profit
from data.data_pre_processing import with_actual_quantities
from data.gain_calculator import get_gain
from data.sell_profit_calculator import get_sell_profit

MAIN_CURRENCIES = ["BTC", "LTC", "ETH"]


def __get_currency(market):
    return market.replace("BTC-", "")


def __get_total(aggregated_data):
    total_profit = sum(map(lambda x: x[2], aggregated_data))
    return ['TOTAL', '', total_profit]


def get_aggregated_data():
    orders = get_order_history().copy()
    btc_orders = convert_orders_to_btc(orders)
    extended_btc_orders = with_actual_quantities(btc_orders)

    aggregated_data = []

    sorted_by_exchange = sorted(extended_btc_orders, key=lambda x: x["Exchange"])
    for market, group in groupby(sorted_by_exchange, lambda item: item["Exchange"]):
        currency = __get_currency(market)

        if currency in MAIN_CURRENCIES:
            continue

        currency_orders = list(group)
        gain = get_gain(currency_orders)
        sell_profit = get_sell_profit(currency_orders)
        potential_current_profit = get_current_profit(currency_orders, currency)

        aggregated_data += [[currency, gain, sell_profit, potential_current_profit]]

    aggregated_data += [__get_total(aggregated_data)]

    return aggregated_data


def fetch_gains_loop(connection):
    while True:
        aggregated_data = get_aggregated_data()
        connection.send(aggregated_data)
        sleep(10)
