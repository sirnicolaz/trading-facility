import npyscreen

class Converter(npyscreen.ActionPopup):
    DEFAULT_COLUMNS = 100

    def __init__(self, data_pipe, *args, **kwargs):
        super(Converter, self).__init__(*args, **kwargs)
        self.data_pipe = data_pipe

    def create(self):
        self.order = self.add(npyscreen.TitleText, name = "Order:", max_width=30, max_height=1)

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