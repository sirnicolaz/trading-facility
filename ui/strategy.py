import npyscreen


class StrategiesGrid(npyscreen.GridColTitles):
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


class StrategyIndicatorsForm(npyscreen.Form):
    #def __init__(self, data_producer, input_queue, *args, **kwargs):
    #    super(StrategyIndicatorsForm, self).__init__(*args, **kwargs)
    #    self.data_producer = data_producer
    #    self.input_queue = input_queue

    def while_waiting(self):
        pass
        #if self.data_producer.poll():
        #    self.strategies.refresh(self.data_producer.recv())

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.markets_selection = self.add(npyscreen.MultiSelectFixed, values=["BTC-ETH", "BTC-QTUM"])
        self.strategies = self.add(StrategiesGrid,
                              col_titles=["market", "stoch_rsi"],
                              columns=1, select_whole_line=True, row_height=2,
                              values=[["Loading...","Loading..."]])