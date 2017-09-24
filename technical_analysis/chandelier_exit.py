import talib
import numpy as np


def _get_numpy_array_for(data, field):
    return np.array(list(map(lambda x: x[field], data)))


def get_long_chandelier_exit(data, period=22, coefficient=3):
    high = _get_numpy_array_for(data, 'high')
    low = _get_numpy_array_for(data, 'low')
    close = _get_numpy_array_for(data, 'close')
    period_high =  max(map(lambda x: x['high'], data[-period:]))
    atr = talib.ATR(high, low, close, timeperiod=period)

    chandelier_exit_price = period_high - atr[-1] * coefficient

    return chandelier_exit_price
