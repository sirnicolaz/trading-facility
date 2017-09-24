from api import historical_api
from technical_analysis.chandelier_exit import get_long_chandelier_exit
from api.account_api import get_balance
from bots import _private_apis_handler
import time


def dynamic_stop_loss_loop(currency):
    balance = float(get_balance(currency)['Balance'])
    while balance > 0.0:
        datapoints = historical_api.get_historical_hour(currency, "BTC", limit=60)
        exit_price = get_long_chandelier_exit(datapoints, coefficient=3)

        print(exit_price)
        time.sleep(10)


def run(*argv):
    currency = argv[0]
    _private_apis_handler.start()
    dynamic_stop_loss_loop(currency)
