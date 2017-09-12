from helpers.order_utilities import *

__PRECISION = 12


def get_sell_profit(orders):
    buys = only_buys(orders)
    sells = only_sells(orders)

    total_profit_btc = 0
    for sell in reversed(sells):
        sell_capacity = sell['ActualQuantity']
        sell_price = sell['PricePerUnit']
        for buy in reversed(buys):
            if sell_capacity <= 0:
                break

            buy_price = buy['PricePerUnit']
            sold_amount = min(sell_capacity, buy['ActualQuantity'])
            earned_btc = sold_amount * sell_price
            partial_profit_btc = earned_btc - (sold_amount * buy_price)
            total_profit_btc = round(total_profit_btc + partial_profit_btc, __PRECISION)

            sell_capacity -= sold_amount
            buy['ActualQuantity'] -= sold_amount

    return total_profit_btc

