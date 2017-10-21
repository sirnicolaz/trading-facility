import ta_trackers.looper as looper
from utilities.market_helpers import market_for_currency
from technical_analysis.rsi import get_rsi


def run(*argv):
    currency = argv[0]
    timeframe = int(argv[1]) if len(argv) > 1 else 4

    return get_rsi(market_for_currency(currency), aggregate=timeframe)[-1], "rsi_%s" % currency


if __name__ == "__main__":
    looper.run_loop(run)
