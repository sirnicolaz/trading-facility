# Trading Facility

Currenty supports only Bittrex.

# Setup
## Dependencies
Run
`sh setup.sh`
to install all the required dependencies. Python 3.5+ required.

## API credentials
The following environment variables have to be se in order to see you own Bittrex account information:
```
API_KEY=xxxx
API_SECRET=xxxx
```
You can create the API key and secret in your own account. Make sure you give writing permissions if you want to be able to place orders via the cui or the bots.
## Order history
Due to the bad implementation of the Bittrex APIs, only orders from the last month can be retrieved.
In order to fix this, you need to get your orders via the private apis
```
https://bittrex.com/Api/v2.0/auth/orders/GetOrderHistory
```
Authentication cookies are required. Also, the json response has to be converted into a csv (not sure why this dumb decision).
This will all be fixed and simplified soon. You can use the app also without this file and it will
just work with the last month of orders. In case you decide to get your orders from Bittrex directly, set the following env:
```
ORDER_HISTORY_FILE=path to your order csv file
```

## Bittrex private API proxy

In order to be able to place conditional sell orders (necessary for dynamic stop losses), you need to start the proxy.
Before doing this, authenticate via web into the Bittrex dashboard and then copy the whole authentication cookie
to cookies.txt (inside the root directory).
After that run:
```
python start_proxy.py
```
While the proxy runs, it will refresh the authentication cookies. If you stop if for a while, you will probably have
to get again the cookies manually from the browser.

# The console user interface (CUI)
The app comes with a console dashboard to have an overview of the current coins that has been traded
on. Start it with:
```
python start_cui.py
```
New orders will not be immediately visible in the interface, due to caching. If you are in a rush, just
restart it.

# Bots
TODO. You can try to figure it out yourself in the meantime by looking at `run_bot.py`
