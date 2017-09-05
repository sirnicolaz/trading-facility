from data.api.account_api import get_balance
from data.api.public_api import get_ticker
from data import sell_profit_calculator
from data import data_pre_processing

def get_current_profit(orders, currency):
    balance = get_balance(currency)
    ticker = get_ticker("BTC-" + currency)
    last_price = ticker["Last"]

    # Add artificial sell order to simulate what would be the gain if selling all now
    fake_order = [{
        'OrderType': 'LIMIT_SELL',
        'ActualQuantity': balance['Available'],
        'PricePerUnit': last_price
    }]

    squashed_orders = data_pre_processing.squash_sells_into_buys(orders)
    new_profit = sell_profit_calculator.get_sell_profit(fake_order + squashed_orders)

    return new_profit