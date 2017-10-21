import talib
import numpy as np
from api import historical_api


def get_rsi(market, aggregate):
    period = 14
    from_currency = market[market.index("-")+1:]
    to_currency = market[:market.index("-")]

    data = historical_api.get_historical_hour(from_currency, to_currency, limit=200, aggregate=aggregate)
    close = np.array([d['close'] for d in data])
    values = talib.RSI(close, period)

    return values


def is_overssold(rsi_values):
    return rsi_values <= 30


def is_overbought(rsi_values):
    return rsi_values >=70

