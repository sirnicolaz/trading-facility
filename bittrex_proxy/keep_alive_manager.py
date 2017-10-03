from random import randint
from time import sleep

from bittrex_proxy.private_api import is_alive


def keep_alive_loop():
    while True:
        # Add a simple keep alive request to the loop. Randomize time
        if is_alive() == False:
            break

        sleep(randint(10, 60))

