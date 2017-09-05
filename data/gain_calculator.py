from data import data_pre_processing
from data.api.public_api import *
from data.api.account_api import *
from data.fin_math import percentage_gain


def __get_gain_for_order(order, current_value):
    units = order['ActualQuantity']
    buy_price = order['PricePerUnit']

    gain = percentage_gain(current_value, buy_price)

    return [gain, units]


def __get_current_currencies():
    balances = get_balances()
    return [balance['Currency'] for balance in balances]


def __get_gain_for_currency(buy_orders):
    current_value = get_ticker(buy_orders[0]['Exchange'])['Last']

    total_gain = 0
    total_units = 0

    for order in buy_orders:
        gain, units = __get_gain_for_order(order, current_value)
        total_gain += gain * units
        total_units += units

    overall_gain = float(total_gain) / float(total_units) if total_units > 0 else 0

    return overall_gain


def get_gain(orders):
    buy_orders = data_pre_processing.squash_sells_into_buys(orders)

    return __get_gain_for_currency(buy_orders)
