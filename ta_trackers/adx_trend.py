import ta_trackers.looper as looper
from utilities.market_helpers import market_for_currency
from technical_analysis.adx import get_adx, get_minus_di, get_plus_di, is_trend_down


def run(*argv):
    currency = argv[0]
    timeframe = int(argv[1]) if len(argv) > 1 else 4

    adx = get_adx(market_for_currency(currency), aggregate=timeframe)
    plus_di = get_plus_di(market_for_currency(currency), aggregate=timeframe)
    minus_di = get_minus_di(market_for_currency(currency), aggregate=timeframe)
    trend_values = ["up", "down"]

    trend_down = is_trend_down(minusdi=minus_di, plusdi=plus_di)
    return "%s - %.2f" % (trend_values[trend_down], adx[-1]), "adx-trend_%s" % currency


if __name__ == "__main__":
    looper.run_loop(run)
