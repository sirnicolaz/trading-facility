from environment import REFERENCE_CURRENCY
from ui.controllers.search_action_controller import ActionControllerSearch
import npyscreen
import datetime
import operator
import webbrowser


class CoinsIndicatorsGrid(npyscreen.GridColTitles):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            "col_titles": ["market", "RSI", "MACD trend", "ADX trend", "twitter"],
            "columns": 5,
            "select_whole_line": True,
            "row_height": 1
        })
        super(CoinsIndicatorsGrid, self).__init__(*args, **kwargs)

    def custom_print_cell(self, actual_cell, cell_display_value):
        try:
            value = cell_display_value

            if "down" in value:
                actual_cell.color = 'DANGER'
            elif "up" in value:
                actual_cell.color = 'GOOD'
            elif float(value) < 30.0:
                actual_cell.color = 'DANGER'
            elif float(value) > 70.0:
                actual_cell.color = 'GOOD'
            else:
                actual_cell.color = 'CONTROL'

        except ValueError:
            actual_cell.color = 'CONTROL'


class CoinsIndicators(npyscreen.FormMuttActive):
    MAIN_WIDGET_CLASS = CoinsIndicatorsGrid
    MAIN_WIDGET_CLASS_START_LINE = 2
    ACTION_CONTROLLER = ActionControllerSearch
    COMMAND_WIDGET_CLASS = npyscreen.TextCommandBox

    def __init__(self, data_producer, *args, **kwargs):
        super(CoinsIndicators, self).__init__(*args, **kwargs)
        self.data_producer = data_producer
        self.markets = {}
        self.searched_markets = {}
        self.filter = False

    def beforeEditing(self):
        self.wMain.values = [["Loading...", "Loading..."]]
        self.wMain.display()
        self.wStatus2.value = "search"
        self.update_title()
        self.add_handlers({
            "f": self.filter_toggle,
        })

    def update_title(self, atime=None):
        title = "coin indicators board (%s)" % REFERENCE_CURRENCY
        if atime:
            title = "%s - last updated %s" % (title, atime.strftime("%Y-%m-%d %H:%M:%S"))

        self.wStatus1.value = title
        self.wStatus1.display()

    def refresh_data(self):
        while not self.data_producer.empty():
            data = self.data_producer.get()
            if "exception" in data:
                self.wStatus2.value = "Exception fetching data: %s" % data["exception"]
            else:

                market = data.pop("market")
                rsi_value = data["rsi"]
                if float(rsi_value) > 0:
                    self.markets[market] = data

        self.refresh_main_view()

    def refresh_main_view(self):
        markets = self.markets
        if self.filter:
            markets = dict(filter(lambda item: float(item[1]["rsi"]) <= 30 or
                                               float(item[1]["rsi"]) >= 70,
                                  markets.items()))

        if len(self.searched_markets) > 0:
            searched_markets_string = "%".join(self.searched_markets.keys())
            markets = dict(filter(lambda market: market[0] in searched_markets_string, markets.items()))

        grid_values = [[market, indicators["rsi"], indicators["macd-trend"],
                        indicators["adx-trend"], indicators["twitter"]] for market, indicators in markets.items()]
        sorted_grid_values = sorted(grid_values, key=operator.itemgetter(1))

        self.wMain.values = sorted_grid_values
        self.update_title(datetime.datetime.now())
        self.wMain.update()

    def while_waiting(self):
        self.refresh_data()

    def filter_toggle(self, *args, **keywords):
        self.filter = not self.filter


