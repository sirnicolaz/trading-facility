from flask import Flask
from flask import request, jsonify
from bittrex_proxy import private_api
from multiprocessing import Queue
from threading import Thread

import bittrex_proxy.private_api
from bittrex_proxy.keep_alive_manager import keep_alive_loop
from bittrex_proxy.private_api_manager import request_handling_loop


app = Flask(__name__)


# Kept GET method for uniformity with bittrex APIs
@app.route('/conditional_sell')
def put_conditional_sell():
    market = request.args.get('market')
    quantity = request.args.get('quantity')
    rate = request.args.get('rate')
    target = request.args.get('target')

    response = private_api.put_conditional_sell_limit(market, quantity, rate, target)

    return jsonify(response)


@app.route('/is_alive')
def is_alive():
    return jsonify({"alive": private_api.is_alive()})


def start(authenticated_cookies_file):
    # Hack to use the private APIs that provide conditional orders
    queue = Queue()
    bittrex_proxy.private_api.set_queue(queue)
    request_handler = Thread(target=request_handling_loop, args=(queue, authenticated_cookies_file))
    keep_alive_handler = Thread(target=keep_alive_loop)
    request_handler.start()
    keep_alive_handler.start()

    app.run(port=4242)
