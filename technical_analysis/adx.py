import talib
import numpy as np
from api import historical_api


def __extract(key, data):
    return np.array([d[key] for d in data])


def __get_data(market, aggregate):
    from_currency = market[market.index("-") + 1:]
    to_currency = market[:market.index("-")]

    data = historical_api.get_historical_hour(from_currency, to_currency, limit=200, aggregate=aggregate)

    close = __extract("close", data)
    high = __extract("high", data)
    low = __extract("low", data)

    return close, high, low


def get_plus_di(market, aggregate):
    close, high, low = __get_data(market, aggregate)
    values = talib.PLUS_DI(high, low, close, timeperiod=14)

    return values


def get_minus_di(market, aggregate):
    close, high, low = __get_data(market, aggregate)
    values = talib.MINUS_DI(high, low, close, timeperiod=14)

    return values


def get_adx(market, aggregate):
    close, high, low = __get_data(market, aggregate)
    values = talib.ADX(high, low, close, timeperiod=14)

    return values


def is_trend_down(plusdi, minusdi):
    return minusdi[-1] > plusdi[-1]
