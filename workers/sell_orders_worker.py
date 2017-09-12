from data.order_manager import sell_all_limit, cancel_all_opened_sell_orders


def put_sell_all_limit_order(market, rate):
    cancel_all_opened_sell_orders(market)
    return sell_all_limit(market, rate)


def put_order_loop(connection):
    while True:
        try:
            query = connection.recv()
            market = query["market"]
            type = query["type"]
            if type != "limit":
                raise ValueError("Only limit orders currently supported")

            rate = float(query["rate"])
            result = put_sell_all_limit_order(market=market, rate=rate)
            if result['success'] == 'true':
                connection.send({'success': True})
            else:
                raise Exception(result['message'])
        except Exception as e:
            connection.send({"exception": str(e)})