from environment import REFERENCE_CURRENCY


def extract_currency(market):
    return market[market.index("-")+1:]


def market_for_currency(currency):
    return (REFERENCE_CURRENCY + "-" + currency).upper()