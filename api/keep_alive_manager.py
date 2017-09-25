from random import randint
from time import sleep
from api.private_api import is_alive


def keep_alive_loop():
    while True:
        # Add a simple keep alive request to the loop. Randomize time
        is_alive()
        sleep(randint(10, 20))

