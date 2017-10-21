import ta_trackers.looper as looper
from utilities.market_helpers import market_for_currency
from technical_analysis.macd import get_macd, is_trend_down


def run(*argv):
    currency = argv[0]
    timeframe = int(argv[1]) if len(argv) > 1 else 4

    macd, signal, _ = get_macd(market_for_currency(currency), aggregate=timeframe)
    trend_values = ["up", "down"]
    return trend_values[is_trend_down(macd, signal)], "macd-trend_%s" % currency


if __name__ == "__main__":
    looper.run_loop(run)
