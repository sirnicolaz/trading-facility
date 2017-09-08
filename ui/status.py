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
        self.coins = self.add(CoinsStatusGrid,
                              col_titles=["market", "gain", "sold profit (btc)", "sell all now profit (btc)"],
                              columns=4, select_whole_line=True, row_height=2,
                              values=[["Loading...","Loading...", "Loading...", "Loading..."]])