from time import sleep
from data.gain_calculator import get_gain
from data.api.account_api import get_order_history
from itertools import groupby
from data.api.conversion_utilities import convert_orders_to_btc

MAIN_CURRENCIES = ["BTC", "LTC", "ETH"]


def __get_currency(market):
    return market.replace("BTC-", "")


def fetch_gains_loop(connection):
    while True:
        orders = get_order_history().copy()
        btc_orders = convert_orders_to_btc(orders)

        aggregated_data = []

        sorted_by_exchange = sorted(btc_orders, key=lambda x: x["Exchange"])
        for market, group in groupby(sorted_by_exchange, lambda item: item["Exchange"]):
            currency = __get_currency(market)

            if currency in MAIN_CURRENCIES:
                continue

            currency_orders = list(group)
            gain = get_gain(currency_orders)

            aggregated_data += [[currency, gain]]

        connection.send(aggregated_data)
        sleep(10)