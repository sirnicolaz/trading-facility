from environment import REFERENCE_CURRENCY
from ui.controllers.converter_action_controller import ConvertedActionController
import npyscreen
import datetime


class CoinsStatusGrid(npyscreen.GridColTitles):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            "col_titles": ["market", "last price", "gain", "sold profit", "sell all now profit"],
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

            if actual_cell.grid_current_value_index != -1:
                _, column = actual_cell.grid_current_value_index
                if (column == 2):
                    actual_cell.value = "%.2f%%" % value
                else:
                    actual_cell.value = "%.10f" % value

        except ValueError:
            actual_cell.color = 'CONTROL'


class CoinsStatus(npyscreen.FormMuttActive):
    MAIN_WIDGET_CLASS = CoinsStatusGrid
    MAIN_WIDGET_CLASS_START_LINE = 2
    ACTION_CONTROLLER = ConvertedActionController
    COMMAND_WIDGET_CLASS = npyscreen.TextCommandBox

    def __init__(self, data_producer, *args, **kwargs):
        super(CoinsStatus, self).__init__(*args, **kwargs)
        self.data_producer = data_producer
        self.coin_values = []
        self.add_handlers({
            "c": self.manage_coin,
        })

    def beforeEditing(self):
        self.wMain.values = [["Loading...", "Loading...", "Loading...", "Loading...", "Loading..."]]
        self.wMain.display()
        self.wStatus2.value = "converter"
        self.update_title()

    def update_title(self, atime=None):
        title = "coin status board (%s)" % REFERENCE_CURRENCY
        if atime:
            title = "%s - last updated %s" % (title, atime.strftime("%Y-%m-%d %H:%M:%S"))

        self.wStatus1.value = title
        self.wStatus1.display()

    def refresh_data(self):
        if self.data_producer.poll():
            data = self.data_producer.recv()
            if "exception" in data:
                self.wStatus2.value = "Exception fetching data: %s" % data["exception"]
            else:
                self.coin_values = list(map(lambda x: [x[0], x[1]], data))
                self.wMain.values = data
                self.update_title(datetime.datetime.now())

        self.wMain.update()

    def while_waiting(self):
        self.refresh_data()

    def manage_coin(self, *args, **keywords):
        self.parentApp.getForm('MANAGECOINFM').currency = self.coin_values[self.wMain.edit_cell[0]][0]
        self.parentApp.getForm('MANAGECOINFM').set_current_value(self.coin_values[self.wMain.edit_cell[0]][1])
        self.parentApp.switchForm('MANAGECOINFM')

    #def afterEditing(self):
    #    self.parentApp.setNextForm(None)
