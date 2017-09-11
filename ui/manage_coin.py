import npyscreen


class ManageCoinGrid(npyscreen.GridColTitles):

    def __init__(self, *args, **kwargs):
        kwargs.update({
            "col_titles": ["order %", "order btc", "bid %", "bid btc", "ask %", "ask btc", "last %", "last btc"],
            "columns": 8,
            "select_whole_line": True,
            "row_height": 2
        })
        super(ManageCoinGrid, self).__init__(*args, **kwargs)


class ManageCoin(npyscreen.ActionPopup):
    keypress_timeout_default = 3
    DEFAULT_COLUMNS = 100

    def __init__(self, data_pipe, *args, **kwargs):
        super(ManageCoin, self).__init__(*args, **kwargs)
        self.data_pipe = data_pipe

    def create(self):
        self.currency = None
        self.last_order = None
        self.current_value = None
        self.order = self.add(npyscreen.TitleText, name = "Order:", max_width=30, max_height=1)
        self.nextrely = 4
        self.overview = self.add(ManageCoinGrid, name="Gains", editable=False)
        self.overview.values = [["0", "0", "0", "0", "0", "0", "0", "0"]]
        #self.put_sell_order = self.add(npyscreen.ButtonPress, name = "Put sell order")

    def beforeEditing(self):
        self.name = self.form_name(self.currency, self.current_value)

    def form_name(self, currency, value=None):
        if value is None:
            return "%s" % currency
        else:
            return "%s @%s" % (currency, value)


    def while_waiting(self):
        if self.last_order != self.order.value:
            self.data_pipe.send({"currency": self.currency, "order": self.order.value})
            self.last_order = self.order.value

        if self.data_pipe.poll():
            data = self.data_pipe.recv()
            if not "exception" in data:
                self.overview.values = [data["gains"]]
                self.overview.update()

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()