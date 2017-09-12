from random import randint
from time import sleep



def keep_alive_loop(queue):
    while True:
        # Add a simple keep alive request to the loop. Randomize time
        url = 'https://bittrex.com/Market/Index?MarketName=BTC-PAY'
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'

        queue.put({
            'url': url,
            'accept': accept
        })

        sleep(randint(60, 200))

