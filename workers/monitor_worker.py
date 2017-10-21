from utilities.coins import COINS
from threading import Thread
from environment import COIN_SOCIAL_DIR
from time import sleep
import os.path


def get_file_path(coin, indicator):
    return "/tmp/%s_%s" % (indicator, coin.upper())


def update_coin(coin, connection):
    updates = {"market": "BTC-" + coin}
    indicators = ["rsi", "macd-trend", "adx-trend"]

    for indicator in indicators:
        if os.path.isfile(get_file_path(coin, indicator)):
            with open(get_file_path(coin, indicator), "r") as value:
                value = value.read()
                updates.update({indicator: value})
        else:
            updates.update({indicator: None})

    if any([updates[indicator] is not None for indicator in indicators]):
        try:
            with open(COIN_SOCIAL_DIR + "/" + coin, "r") as file:
                twitter_handle = file.read()
                updates.update({"twitter": twitter_handle})
        except:
            updates.update({"twitter": ""})

        connection.put(updates)


def fetch_indicators(connection):
    while True:
        for coin in COINS:
            update_coin(coin, connection)
            #Thread(target=update_coin, args=(coin, connection))

        sleep(3)