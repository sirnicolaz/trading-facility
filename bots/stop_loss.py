from ._threshold_checker import conditional_sell_loop_stop_loss


def run(*argv):
    currency = argv[0]
    gain = float(argv[1])

    conditional_sell_loop_stop_loss(currency, gain)