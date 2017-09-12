import npyscreen
import datetime
import curses


class CoinsStatusGrid(npyscreen.GridColTitles):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            "col_titles": ["market", "current price", "gain", "sold profit", "sell all now profit"],
            "columns": 5,
            "select_whole_line": True,
            "row_height": 2
        })
        super(CoinsStatusGrid, self).__init__(*args, **kwargs)

    def custom_print_cell(self, actual_cell, cell_display_value):
        try:
            value = float(cell_display_value)
            if value < 0.0:
                actual_cell.color = 'DANGER'
            else:
                actual_cell.color = 'GOOD'
        except ValueError:
            actual_cell.color = 'DEFAULT'


class CoinsStatus(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = CoinsStatusGrid
    MAIN_WIDGET_CLASS_START_LINE = 2

    def __init__(self, data_producer, reference_currency, *args, **kwargs):
        super(CoinsStatus, self).__init__(*args, **kwargs)
        self.data_producer = data_producer
        self.reference_currency = reference_currency
        self.coin_values = []
        self.add_handlers({
            "c": self.manage_coin,
        })

    def beforeEditing(self):
        self.wMain.values = [["Loading...", "Loading...", "Loading...", "Loading...", "Loading..."]]
        self.wMain.display()
        self.wStatus1.value = "coin status board (%s)" % self.reference_currency
        self.wStatus2.value = "Loading..."

    def refresh_data(self):
        if self.data_producer.poll():
            data = self.data_producer.recv()
            if "exception" in data:
                self.wStatus2.value = "Exception fetching data: %s" % data["exception"]
            else:
                self.coin_values = list(map(lambda x: [x[0], x[1]], data))
                self.wMain.values = data
                self.wStatus2.value = "Last update %s" % str(datetime.datetime.now())

        self.wMain.update()
        self.wStatus2.update()

    def while_waiting(self):
        self.refresh_data()

    def manage_coin(self, *args, **keywords):
        self.parentApp.getForm('MANAGECOINFM').currency = self.coin_values[self.wMain.edit_cell[0]][0]
        self.parentApp.getForm('MANAGECOINFM').set_current_value(self.coin_values[self.wMain.edit_cell[0]][1])
        self.parentApp.switchForm('MANAGECOINFM')

    #def afterEditing(self):
    #    self.parentApp.setNextForm(None)
