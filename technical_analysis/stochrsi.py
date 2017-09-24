import talib
import numpy as np
from api import historical_api


def stoch_rsi(market):
    period = 14
    from_currency = market[market.index("-")+1:]
    to_currency = market[:market.index("-")]

    data = historical_api.get_historical_hour(from_currency, to_currency)
    close = np.array([d['close'] for d in data])
    values = talib.STOCHRSI(close, timeperiod=period, fastk_period=3, fastd_period=3, fastd_matype=0)

    return values


def is_overssold(stoch_rsi_values):
    return stoch_rsi_values[0][-1] <= 20 and stoch_rsi_values[1][-1] <= 20


def is_overbought(stoch_rsi_values):
    return stoch_rsi_values[0][-1] >= 80 and stoch_rsi_values[1][-1] >= 80

