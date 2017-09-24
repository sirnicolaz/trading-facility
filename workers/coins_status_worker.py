from itertools import groupby
from time import sleep
from controllers.orders_controller import consolidated_user_orders
from controllers.profit_calculator import get_current_profit, get_achieved_profit
from controllers.gain_calculator import get_current_gain
from api.public_api import get_ticker
from utilities.market_helpers import extract_currency


MAIN_CURRENCIES = ["BTC", "LTC", "ETH"]


def __get_total(aggregated_data):
    total_profit = sum(map(lambda x: x[3], aggregated_data))
    return ['TOTAL', '', '', total_profit]


def get_aggregated_data():
    orders = consolidated_user_orders()
    aggregated_data = []

    sorted_by_exchange = sorted(orders, key=lambda x: x["Exchange"])
    for market, group in groupby(sorted_by_exchange, lambda item: item["Exchange"]):
        currency = extract_currency(market)
        if currency in MAIN_CURRENCIES:
            continue

        ticker = get_ticker(market)
        if ticker is None:
            continue

        currency_orders = list(group)
        gain = get_current_gain(currency_orders)
        sell_profit = get_achieved_profit(currency_orders)
        potential_current_profit = get_current_profit(currency_orders, currency)
        current_value = ticker['Last']

        aggregated_data += [[currency, current_value, gain, sell_profit, potential_current_profit]]

    aggregated_data += [__get_total(aggregated_data)]

    return aggregated_data


def fetch_coins_status_loop(connection):
    while True:
        try:
            aggregated_data = get_aggregated_data()
            connection.send(aggregated_data)
        except Exception as e:
            connection.send({"exception": str(e)})
        sleep(10)
