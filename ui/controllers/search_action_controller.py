import npyscreen
import webbrowser


class ActionControllerSearch(npyscreen.ActionControllerSimple):
    def __init__(self, *args, **kwargs):
        super(ActionControllerSearch, self).__init__(*args, **kwargs)
        self.add_action(ident=".*", function=self.filter, live=True)
        self.add_action(ident="open .* \.", function=self.open_coin, live=True)

    def filter(self, search_keywords, control_widget_proxy, live):
        if search_keywords.startswith("open"):
            return

        keywords = list(filter(None, search_keywords.split(" ")))
        self.parent.searched_markets = dict(filter(
            lambda item: any([keyword in item[0] for keyword in keywords]),
               self.parent.markets.items()))
        self.parent.refresh_main_view()

    def open_coin(self, search_keywords, control_widget_proxy, live):
        coins = list(filter(None, search_keywords.split(" ")))[1:-1]
        print(coins)
        for coin in coins:
            twitter_url = self.parent.markets[coin]['twitter']
            if twitter_url is not None:
                webbrowser.open(twitter_url)

            param = "".join(reversed(coin.split("-")))
            webbrowser.open("https://www.tradingview.com/chart/?symbol=BITTREX:%s" % param)