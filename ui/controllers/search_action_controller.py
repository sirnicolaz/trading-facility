import npyscreen


class ActionControllerSearch(npyscreen.ActionControllerSimple):
    def __init__(self, *args, **kwargs):
        super(ActionControllerSearch, self).__init__(*args, **kwargs)
        self.add_action(ident=".*", function=self.filter, live=True)

    def filter(self, search_keywords, control_widget_proxy, live):
        keywords = list(filter(None, search_keywords.split(" ")))
        self.parent.searched_markets = dict(filter(
            lambda item: any([keyword in item[0] for keyword in keywords]),
               self.parent.markets.items()))
        self.parent.refresh_main_view()