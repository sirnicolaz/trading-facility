BASE_URL = "https://bittrex.com/api/v1.1/"
PUBLIC_API = BASE_URL + "public/"
ACCOUNT_API = BASE_URL + "account/"


class PublicEndpoints:
    @staticmethod
    def get_markets():
        return PUBLIC_API + "getmarkets"

    @staticmethod
    def get_currencies():
        return PUBLIC_API + "getcurrencies"

    @staticmethod
    def get_ticker(market):
        return PUBLIC_API + "getticker?market=%s" % market

    @staticmethod
    def get_market_summaries():
        return PUBLIC_API + "getmarketsummaries"

    @staticmethod
    def get_market_summary(market):
        return PUBLIC_API + "getmarketsummary?market=%s" % market

    @staticmethod
    # type = buy, sell or both
    def get_order_book(market, type):
        return PUBLIC_API + "getorderbook?market=%s&type=%s" % (market, type)

    @staticmethod
    def get_market_history(market):
        return PUBLIC_API + "getmarkethistory?market=%s" % market


class AccountEndpoints:
    @staticmethod
    def get_balances():
        return ACCOUNT_API + "getbalances"

    @staticmethod
    def get_balance(currency):
        return ACCOUNT_API + "getbalance?currency=%s" % currency

    @staticmethod
    def get_order_history(market=None):
        if market:
            return ACCOUNT_API + "getorderhistory?market=%s" % market
        else:
            return ACCOUNT_API + "getorderhistory"

    @staticmethod
    def get_order(order_uuid):
        return ACCOUNT_API + "getorder?uuid=%s" % order_uuid

