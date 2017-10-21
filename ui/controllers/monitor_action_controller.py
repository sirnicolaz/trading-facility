import npyscreen
import webbrowser


class MonitorActionController(npyscreen.ActionControllerSimple):
    def __init__(self, *args, **kwargs):
        super(MonitorActionController, self).__init__(*args, **kwargs)
        self.add_action(ident="search .*", function=self.filter, live=True)
        self.add_action(ident="open .* =", function=self.open_coin, live=True)

    def filter(self, search_keywords, control_widget_proxy, live):
        if not search_keywords.startswith("search"):
            return

        keywords = list(filter(None, search_keywords.split(" ")))
        self.parent.searched_markets = dict(filter(
            lambda item: any([keyword in item[0] for keyword in keywords]),
               self.parent.markets.items()))
        self.parent.refresh_main_view()

    def open_coin(self, search_keywords, control_widget_proxy, live):
        if not search_keywords.startswith("open"):
            return

        coins = list(filter(None, search_keywords.split(" ")))[1:-1]
        total_opened_links = 0
        for coin in coins:
            coin_only = coin.split("-")[-1]
            twitter_url = self.parent.markets["BTC-" + coin_only]['twitter']
            if twitter_url is not None:
                webbrowser.open(twitter_url)
                total_opened_links += 1

            webbrowser.open("https://www.tradingview.com/chart/?symbol=BITTREX:%sBTC" % coin_only)
            total_opened_links += 1

        control_widget_proxy.value = "%s total opened links %d" % (search_keywords, total_opened_links)
