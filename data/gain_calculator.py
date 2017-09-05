from data import data_pre_processing
from data.api.conversion_utilities import convert_orders_to_btc
from data.api.public_api import *
from data.api.account_api import *


def __get_gain_for_order(order, current_value):
    units = order['Quantity']
    buy_price = order['PricePerUnit']

    gain = (current_value * 100.0 / buy_price) - 100.0

    return [gain, units]


def __get_current_currencies():
    balances = get_balances()
    return [balance['Currency'] for balance in balances]


def get_gain_for_currency(orders, currency):
    if currency == "BTC":
        return 0

    current_value = get_ticker("BTC-" + currency)['Last']
    currency_sells = list(filter(lambda order: order['OrderType'] == 'LIMIT_SELL', orders))
    currency_buys = list(filter(lambda order: order['OrderType'] == 'LIMIT_BUY', orders))

    total_gain = 0
    total_units = 0

    # remove sells from buys
    currency_buys = data_pre_processing.subtract_sells_from_buys(currency_sells, currency_buys)

    for order in currency_buys:
        gain, units = __get_gain_for_order(order, current_value)
        total_gain += gain * units
        total_units += units

    overall_gain = float(total_gain) / float(total_units) if total_units > 0 else 0

    return overall_gain


def get_all_gains():
    currencies = __get_current_currencies().copy()
    orders = get_order_history().copy()

    # Normalization
    orders = data_pre_processing.repair_quantities(orders)
    orders = convert_orders_to_btc(orders)

    data = []
    for currency in currencies:
        currency_orders = list(filter(lambda order: "-" + currency.lower() in order['Exchange'].lower(), orders))
        data += [[currency, get_gain_for_currency(currency_orders, currency)]]

    return data