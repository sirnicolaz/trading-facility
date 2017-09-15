from ._threshold_checker import conditional_sell_loop_take_profit


def run(*argv):
    currency = argv[0]
    gain = float(argv[1])

    conditional_sell_loop_take_profit(currency, gain)