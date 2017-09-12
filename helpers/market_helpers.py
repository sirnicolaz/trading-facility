def extract_currency(market, reference_currency="btc"):
    return market.replace("%s-" % reference_currency.upper(), "")