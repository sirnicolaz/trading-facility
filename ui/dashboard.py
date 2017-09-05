import npyscreen


class CoinsStatusGrid(npyscreen.GridColTitles):
    def refresh(self, new_data):
        data = list(sum(new_data, []))
        self.set_grid_values_from_flat_list(new_values=data, reset_cursor=False)

    def custom_print_cell(self, actual_cell, cell_display_value):
        try:
            value = float(cell_display_value)
            if value < 0.0:
                actual_cell.color = 'DANGER'
            else:
                actual_cell.color = 'GOOD'
        except ValueError:
            actual_cell.color = 'DEFAULT'


class CoinsStatus(npyscreen.Form):
    def __init__(self, data_producer, *args, **kwargs):
        super(CoinsStatus, self).__init__(*args, **kwargs)
        self.data_producer = data_producer

    def while_waiting(self):
        if self.data_producer.poll():
            self.coins.refresh(self.data_producer.recv())

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.coins = self.add(CoinsStatusGrid, col_titles=["market", "gain", "sell profit (btc)"],
                              columns=3, select_whole_line=True, row_height=2,
                              values=[["Loading...","Loading..", "Loading..."]])


class Dashboard(npyscreen.NPSAppManaged):
    keypress_timeout_default = 10

    def __init__(self, data_producer, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)
        self.data_producer = data_producer

    def onStart(self):
        self.addForm('MAIN', CoinsStatus, data_producer=self.data_producer,
                     name='Coin status dashboard', editable=False)


if __name__ == '__main__':
    dashboard = Dashboard().run()