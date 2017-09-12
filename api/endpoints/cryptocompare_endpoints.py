BASE_URL= "https://min-api.cryptocompare.com"
DATA_API = BASE_URL + "/data"

class HistoricalEndpoints:
    @staticmethod
    def __absolute_url(path):
        return DATA_API + path

    @staticmethod
    def get_history_hour(from_currency, to_currency, limit):
        return HistoricalEndpoints.__absolute_url("/histohour?fsym=%s&tsym=%s&limit=%s&e=BitTrex"
                                                  % (from_currency, to_currency, limit))

    @staticmethod
    def get_price_historical(from_currency, to_currency, timestamp):
        return HistoricalEndpoints.__absolute_url("/pricehistorical?fsym=%s&tsyms=%s&ts=%s&extraParams=trading_facility"
                                                  % (from_currency, to_currency, timestamp))


