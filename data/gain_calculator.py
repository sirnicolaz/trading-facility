from data import data_pre_processing
from data.api.public_api import *
from data.api.account_api import *


def __get_gain_for_order(order, current_value):
    units = order['ActualQuantity']
    buy_price = order['PricePerUnit']

    gain = (current_value * 100.0 / buy_price) - 100.0

    return [gain, units]


def __get_current_currencies():
    balances = get_balances()
    return [balance['Currency'] for balance in balances]


def get_gain_for_currency(buy_orders, currency):
    if currency == "BTC":
        return 0

    current_value = get_ticker("BTC-" + currency)['Last']

    total_gain = 0
    total_units = 0

    for order in buy_orders:
        gain, units = __get_gain_for_order(order, current_value)
        total_gain += gain * units
        total_units += units

    overall_gain = float(total_gain) / float(total_units) if total_units > 0 else 0

    return overall_gain


def get_all_gains():
    currencies = __get_current_currencies().copy()
    orders = get_order_history().copy()

    buy_orders = data_pre_processing.only_buys_with_actual_quantitiy(orders)

    data = []
    for currency in currencies:
        currency_orders = list(filter(lambda buy: "-" + currency.lower() in buy['Exchange'].lower(), buy_orders))
        data += [[currency, get_gain_for_currency(currency_orders, currency)]]

    return data