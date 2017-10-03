import os

API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
REFERENCE_CURRENCY = os.environ.get('REFERENCE_CURRENCY', 'btc')
ORDER_HISTORY_FILE = os.environ.get('ORDER_HISTORY_FILE')
BITTREX_PROXY_URL = os.environ.get("BITTREX_PROXY_URL", "http://localhost:4242/")