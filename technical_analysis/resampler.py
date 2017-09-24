from technical_analysis.utilities import get_list_for


def __pool_data(data, field, pooling_fun):
    pooled_data = map(lambda group: pooling_fun(get_list_for(group, field)), data)

    return list(pooled_data)


def resample(hourly_data, new_timeframe):
    # new_timeframe = 4 hours
    data = list(reversed(hourly_data)) # from newest to oldest
    grouped_data = [data[i:i + new_timeframe] for i in range(0, len(data), new_timeframe)]

    if len(grouped_data[-1]) < new_timeframe:
        grouped_data.pop()

    new_highs = __pool_data(grouped_data, "high", max)
    new_lows = __pool_data(grouped_data, "low", min)
    new_closes = __pool_data(grouped_data, "close", lambda x: x[0])
    new_volumefroms = __pool_data(grouped_data, "volumefrom", lambda x: x[-1])
    new_volumetos = __pool_data(grouped_data, "volumeto", lambda x: x[0])

    return list(reversed([{
        "high": new_highs[index],
        "low": new_lows[index],
        "volumefrom": new_volumefroms[index],
        "volumeto": new_volumetos[index],
        "close": new_closes[index]
    } for index, _ in enumerate(grouped_data)]))

