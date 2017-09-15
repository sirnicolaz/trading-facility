from data.gain_calculator import get_current_gain_for_currency
from data.order_maker import force_put_sell_all_limit_order
from utilities.market_helpers import market_for_currency
from api.public_api import get_ticker
import time


def is_limit_achieved(currency, threshold, compare_fun):
    gain = get_current_gain_for_currency(currency)

    return compare_fun(gain, threshold)


def conditional_sell_loop_wrapper(compare_fun):
    def conditional_sell_loop(currency, threshold):
        while not is_limit_achieved(currency, threshold, compare_fun):
            time.sleep(5)

        market = market_for_currency(currency)
        current_price = get_ticker(market)['Last']
        print("Sell order for %s @%s" % (currency, str(current_price)))
        force_put_sell_all_limit_order(market, current_price)

    return conditional_sell_loop


conditional_sell_loop_take_profit = conditional_sell_loop_wrapper(lambda gain, threshold: gain >= threshold)
conditional_sell_loop_stop_loss = conditional_sell_loop_wrapper(lambda gain, threshold: gain <= threshold)
