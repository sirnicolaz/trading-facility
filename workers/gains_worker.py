from api.public_api import get_ticker
from data.data_pre_processing import simplified_user_orders
from data.gain_calculator import get_gain
from data.profit_calculator import get_profit
from helpers.order_utilities import orders_for_currency


def calculate_gains(currency, order_value):
    ticker = get_ticker("BTC-" + currency)
    orders = simplified_user_orders()

    currency_orders = orders_for_currency(orders, currency)

    order_gain = get_gain(currency_orders, order_value)
    ask_gain = get_gain(currency_orders, ticker["Ask"])
    bid_gain = get_gain(currency_orders, ticker["Bid"])
    last_gain = get_gain(currency_orders, ticker["Last"])

    order_profit = get_profit(currency_orders, currency, order_value)
    ask_profit = get_profit(currency_orders, currency, ticker["Ask"])
    bid_profit = get_profit(currency_orders, currency, ticker["Bid"])
    last_profit = get_profit(currency_orders, currency, ticker["Last"])

    return [order_gain, order_profit, ask_gain, ask_profit, bid_gain, bid_profit, last_gain, last_profit]


def fetch_gains_loop(connection):
    while True:
        try:
            if connection.poll(timeout=3):
                query = connection.recv()
                currency = query["currency"]
                try:
                    order = float(query["order"])
                except ValueError:
                    order = 0

                gains = calculate_gains(currency, order)
                connection.send({"gains": gains})
        except Exception as e:
            connection.send({"exception": str(e)})