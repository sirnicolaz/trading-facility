from api import historical_api
from technical_analysis.chandelier_exit import get_long_chandelier_exit
from technical_analysis.resampler import resample
from api.market_api import put_conditional_sell_limit
from utilities.market_helpers import market_for_currency
from controllers.order_maker import cancel_all_opened_sell_orders
from api.account_api import get_balance
from bots import _private_apis_handler
import time


def dynamic_stop_loss_loop(currency, timeframe_hours):
    balance = float(get_balance(currency)['Balance'])
    while balance > 0.0:
        period = 22
        datapoints = historical_api.get_historical_hour(currency, "BTC", limit=timeframe_hours*period+period)
        datapoints = resample(hourly_data=datapoints, new_timeframe=timeframe_hours)
        exit_price = get_long_chandelier_exit(datapoints, period=period)

        print(exit_price)
        market = market_for_currency(currency)
        cancel_all_opened_sell_orders(market)
        put_conditional_sell_limit(market, balance, rate=exit_price, target=exit_price)
        time.sleep(3600)


def run(*argv):
    currency = argv[0]
    timeframe = argv[1] if len(argv) > 1 else 4
    _private_apis_handler.start()
    dynamic_stop_loss_loop(currency, timeframe)
