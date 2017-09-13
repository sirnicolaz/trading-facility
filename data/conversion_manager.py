from environment import REFERENCE_CURRENCY
from api.price_api import get_price
import copy

__PRECISION = 20


def conver_orders_wrapper(from_currency, to_currency):
    def convert_orders(orders):
        copy_orders = copy.deepcopy(orders)
        for order in copy_orders:
            exchange = order['Exchange']
            if "%s-" % from_currency in exchange:
                one_unit_value = get_price(from_currency, to_currency, order['Closed'])
                order['PricePerUnit'] = round(float(order['PricePerUnit']) * float(one_unit_value), __PRECISION)
                order['Price'] = round(float(order['Price']) * float(one_unit_value), __PRECISION)
                order['Exchange'] = order['Exchange'].replace(from_currency, to_currency)

        return copy_orders

    return convert_orders


convert_orders_to_eth = conver_orders_wrapper("BTC", "ETH")
convert_orders_to_btc = conver_orders_wrapper("ETH", "BTC")


def convert_orders_to_reference_currency(orders):
    if REFERENCE_CURRENCY == "btc":
        return convert_orders_to_btc(orders)
    elif REFERENCE_CURRENCY == "eth":
        return convert_orders_to_eth(orders)
