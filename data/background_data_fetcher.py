from time import sleep
from data.gain_calculator import get_all_gains


def fetch_gains_loop(connection):
    while True:
        gains = get_all_gains()
        connection.send(gains)
        sleep(10)