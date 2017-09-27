import npyscreen
from environment import REFERENCE_CURRENCY


class ManageCoinGrid(npyscreen.GridColTitles):

    def __init__(self, *args, **kwargs):
        kwargs.update({
            "col_titles": ["order %", "order abs", "bid %", "bid abs", "ask %", "ask abs", "last %", "last abs"],
            "columns": 8,
            "select_whole_line": True,
            "row_height": 2
        })
        super(ManageCoinGrid, self).__init__(*args, **kwargs)


class ManageCoin(npyscreen.ActionPopup):
    keypress_timeout_default = 3
    DEFAULT_COLUMNS = 100
    DEFAULT_LINES = 16

    def __init__(self, gains_worker_pipe, order_maker_worker_pipe, *args, **kwargs):
        super(ManageCoin, self).__init__(*args, **kwargs)
        self.gains_worker_pipe = gains_worker_pipe
        self.order_maker_worker_pipe = order_maker_worker_pipe

    def create(self):
        self.currency = None
        self.current_value = None
        self.order = self.add(npyscreen.TitleText, name = "order:", max_width=40, max_height=1)
        self.percentage_amount = self.add(npyscreen.TitleText, name="amount %:", value="100.0", max_width=40, max_height=1)
        self.nextrely = 4
        self.order_type = self.add(npyscreen.TitleSelectOne, name = "type:", scroll_exit=True,
                                   slow_scroll=True, max_width=40, max_height=2,
                                   values=["stop loss", "take profit"])
        self.nextrely = 8
        self.overview = self.add(ManageCoinGrid, name="gains", editable=False)
        self.overview.values = [["0", "0", "0", "0", "0", "0", "0", "0"]]

    def set_current_value(self, current_value):
        self.current_value = current_value
        self.order.value = "%.15f" % float(current_value)

    def beforeEditing(self):
        self.name = self.form_name(self.currency, self.current_value)

    def form_name(self, currency, value=None):
        if value is None:
            return "%s" % currency
        else:
            return "%s @%s" % (currency, value)

    def while_waiting(self):
        query = {"currency": self.currency, "order": self.order.value}
        self.gains_worker_pipe.send(query)

        if self.gains_worker_pipe.poll():
            data = self.gains_worker_pipe.recv()
            if not "exception" in data:
                self.overview.values = [data["gains"]]
                self.overview.update()
            else:
                npyscreen.notify_confirm(data["exception"])

    def on_ok(self):
        order_type = ["stop_loss", "take_profit"][self.order_type.value[0]]
        query = {"rate": self.order.value, "currency": self.currency,
                 "type": order_type, "percentage_amount": self.percentage_amount.value}
        answer = npyscreen.notify_yes_no("You are going to place the following order:\n%s to %s @ %s\norder type: %s" \
                                "\nDo you want to confirm?" %
                                (self.currency.upper(), REFERENCE_CURRENCY.upper(), self.order.value, order_type))
        if answer == True:
            self.order_maker_worker_pipe.send(query)
            self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()