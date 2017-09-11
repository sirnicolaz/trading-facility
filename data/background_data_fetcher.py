from itertools import groupby
from time import sleep

from api.conversion_utilities import convert_orders_to_btc
from api.account_api import get_order_history
from data.profit_calculator import get_profit
from data.data_pre_processing import with_actual_quantities
from data.gain_calculator import get_gain
from data.sell_profit_calculator import get_sell_profit
from api.public_api import get_ticker


MAIN_CURRENCIES = ["BTC", "LTC", "ETH"]


def __get_currency(market):
    return market.replace("BTC-", "")


def __get_total(aggregated_data):
    total_profit = sum(map(lambda x: x[3], aggregated_data))
    return ['TOTAL', '', '', total_profit]


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

        current_value = get_ticker(market)['Last']
        currency_orders = list(group)
        gain = get_gain(currency_orders, current_value)
        sell_profit = get_sell_profit(currency_orders)
        potential_current_profit = get_profit(currency_orders, currency, current_value)

        aggregated_data += [[currency, current_value, gain, sell_profit, potential_current_profit]]

    aggregated_data += [__get_total(aggregated_data)]

    return aggregated_data


def fetch_gains_loop(connection):
    while True:
        try:
            aggregated_data = get_aggregated_data()
            connection.send(aggregated_data)
        except Exception as e:
            connection.send({"exception": str(e)})
        sleep(10)
