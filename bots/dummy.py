from random import random
from api.account_api import get_balance
from bots import _private_apis_handler
from api.market_api import put_conditional_sell_limit
from controllers.order_maker import cancel_all_opened_sell_orders
from utilities.market_helpers import market_for_currency
import time


def dummy_dynamic_stop_loss(currency, max_price):
    balance = float(get_balance(currency)['Balance'])
    while balance > 0.0:
        exit_price = max_price - random() % (max_price / 10)

        market = market_for_currency(currency)
        cancel_all_opened_sell_orders(market)
        put_conditional_sell_limit(market, balance, exit_price, exit_price)

        time.sleep(25)


def run(*argv):
    currency = argv[0]
    max_price = float(argv[1])
    _private_apis_handler.start()
    #dummy_dynamic_stop_loss(currency, max_price)
