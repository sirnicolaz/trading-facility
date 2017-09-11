from api.account_api import get_balance
from api.public_api import get_ticker
from data import data_pre_processing
from data import sell_profit_calculator


def __calculate_profit(orders, currency, sell_price):
    balance = get_balance(currency)

    # Add artificial sell order to simulate what would be the gain if selling all now
    fake_order = [{
        'OrderType': 'LIMIT_SELL',
        'ActualQuantity': balance['Balance'],
        'PricePerUnit': sell_price
    }]

    squashed_orders = data_pre_processing.squash_sells_into_buys(orders)
    new_profit = sell_profit_calculator.get_sell_profit(fake_order + squashed_orders)

    return new_profit


def get_current_profit(orders, currency):
    ticker = get_ticker("BTC-" + currency)
    last_price = ticker["Last"]

    return __calculate_profit(orders=orders, currency=currency, sell_price=last_price)


def get_profit(orders, currency, sell_value):
    return __calculate_profit(orders=orders, currency=currency, sell_price=sell_value)
