from multiprocessing import Queue
from threading import Thread
from api.private_api_manager import request_handling_loop
from api.keep_alive_manager import keep_alive_loop
import api.private_api
import time


def start():
    # Hack to use the private APIs that provide conditional orders
    queue = Queue()
    api.private_api.set_queue(queue)
    request_handler = Thread(target=request_handling_loop, args=(queue,))
    keep_alive_handler = Thread(target=keep_alive_loop)
    request_handler.start()
    time.sleep(1)
    keep_alive_handler.start()
