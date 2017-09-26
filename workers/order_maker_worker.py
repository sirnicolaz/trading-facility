from controllers.order_maker import force_put_conditional_sell_all_order, force_put_sell_all_limit_order
from utilities.market_helpers import market_for_currency


def __place_order(currency, rate, type):
    market = market_for_currency(currency)
    if type == 'stop_loss':
        return force_put_conditional_sell_all_order(market=market, rate=rate)
    elif type == 'take_profit':
        return force_put_sell_all_limit_order(market=market, rate=rate)
    else:
        raise ValueError("Invalid order type: %s" % type)


def make_order_loop(connection):
    while True:
        try:
            query = connection.recv()
            currency = query["currency"]
            rate = float(query["rate"])
            type = query["type"]

            result = __place_order(currency, rate, type)
            connection.send({"result": result})
        except Exception as e:
            connection.send({"exception": str(e)})