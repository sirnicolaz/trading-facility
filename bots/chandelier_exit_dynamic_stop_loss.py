from api import historical_api
from technical_analysis.chandelier_exit import get_long_chandelier_exit
from api import private_api
from utilities.market_helpers import market_for_currency
from controllers.order_maker import cancel_all_opened_sell_orders
from api.account_api import get_balance
from bots import _private_apis_handler
import time


def dynamic_stop_loss_loop(currency, timeframe_hours):
    balance = float(get_balance(currency)['Balance'])
    while balance > 0.0:
        try:
            period = 22
            datapoints = historical_api.get_historical_hour(currency, "BTC", limit=100, aggregate=timeframe_hours)
            exit_price = get_long_chandelier_exit(datapoints, period=period)

            truncated_balance = "%.15f" % balance
            truncated_exit_price = "%.15f" % exit_price
            market = market_for_currency(currency)

            if private_api.is_alive():
                print(exit_price)
                cancel_all_opened_sell_orders(market)
                private_api.put_conditional_sell_limit(market, truncated_balance, rate=truncated_exit_price, target=truncated_exit_price)
            else:
                print("private api currently dead")
        except Exception as e:
            print("temporary failure", str(e))
        time.sleep(60 * 30)


def run(*argv):
    currency = argv[0]
    timeframe = int(argv[1]) if len(argv) > 1 else 4
    _private_apis_handler.start()
    dynamic_stop_loss_loop(currency, timeframe)
