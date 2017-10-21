from time import sleep
from utilities.coins import COINS


def run_loop(handler):
    coins = COINS
    existing_coins = []
    while True:
        for coin in coins:
            try:
                response, metric = handler(coin)
                with open("/tmp/" + metric, "w") as file:
                    file.write(str(response))
                    existing_coins += [coin]
                sleep(1)
            except:
                pass

        coins = existing_coins

