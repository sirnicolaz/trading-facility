from api.account_api import get_balance
from api.public_api import get_ticker
from data import data_pre_processing
from helpers.order_filters import filter_buys, filter_sells, filter_currency
from helpers.market_helpers import market_for_currency


__PRECISION = 12


def __get_profit_for_orders(orders):
    buys = filter_buys(orders)
    sells = filter_sells(orders)

    total_profit_btc = 0
    for sell in reversed(sells):
        sell_capacity = sell['ActualQuantity']
        sell_price = sell['PricePerUnit']
        for buy in reversed(buys):
            if sell_capacity <= 0:
                break

            buy_price = buy['PricePerUnit']
            sold_amount = min(sell_capacity, buy['ActualQuantity'])
            earned_btc = sold_amount * sell_price
            partial_profit_btc = earned_btc - (sold_amount * buy_price)
            total_profit_btc = round(total_profit_btc + partial_profit_btc, __PRECISION)

            sell_capacity -= sold_amount
            buy['ActualQuantity'] -= sold_amount

    return total_profit_btc


def __calculate_profit(orders, currency, sell_price):
    balance = get_balance(currency)

    # Add artificial sell order to simulate what would be the gain if selling all now
    fake_order = [{
        'OrderType': 'LIMIT_SELL',
        'ActualQuantity': balance['Balance'],
        'PricePerUnit': sell_price
    }]

    squashed_orders = data_pre_processing.squash_sells_into_buys(orders)
    new_profit = __get_profit_for_orders(fake_order + squashed_orders)

    return new_profit


def get_achieved_profit(orders):
    return __get_profit_for_orders(orders)


def get_current_profit(orders, currency):
    ticker = get_ticker(market_for_currency(currency))
    last_price = ticker["Last"]

    return __calculate_profit(orders=orders, currency=currency, sell_price=last_price)


def get_profit(orders, currency, sell_value):
    return __calculate_profit(orders=orders, currency=currency, sell_price=sell_value)
