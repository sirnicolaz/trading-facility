from data import data_pre_processing
from data.fin_math import percentage_gain
from api.public_api import get_ticker


def __get_gain_for_order(order, current_value):
    units = order['ActualQuantity']
    buy_price = order['PricePerUnit']

    gain = percentage_gain(current_value, buy_price)

    return [gain, units]


def __get_gain_for_value(buy_orders, value):
    total_gain = 0
    total_units = 0

    for order in buy_orders:
        gain, units = __get_gain_for_order(order, value)
        total_gain += gain * units
        total_units += units

    overall_gain = float(total_gain) / float(total_units) if total_units > 0 else 0

    return overall_gain


def get_current_gain(orders):
    buy_orders = data_pre_processing.squash_sells_into_buys(orders)
    current_value = get_ticker(buy_orders[0]['Exchange'])['Last']

    return __get_gain_for_value(buy_orders, current_value)


def get_gain(orders, new_value):
    buy_orders = data_pre_processing.squash_sells_into_buys(orders)

    return __get_gain_for_value(buy_orders, new_value)