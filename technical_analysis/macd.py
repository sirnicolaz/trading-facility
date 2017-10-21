import talib
import numpy as np
from api import historical_api


def get_macd(market, aggregate):
    from_currency = market[market.index("-")+1:]
    to_currency = market[:market.index("-")]

    data = historical_api.get_historical_hour(from_currency, to_currency, limit=200, aggregate=aggregate)
    close = np.array([d['close'] for d in data])
    values = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

    return values


def is_trend_down(macd, signal):
    return macd[-1] < signal[-1] < 0.0
