import npyscreen
from ui.status import CoinsStatus
from ui.monitor import CoinsIndicators


class MonitorDashboard(npyscreen.NPSAppManaged):
    keypress_timeout_default = 10

    def __init__(self, data_producer, *args, **kwargs):
        super(MonitorDashboard, self).__init__(*args, **kwargs)
        self.data_producer = data_producer

    def onStart(self):
        self.addForm('MAIN', CoinsIndicators, data_producer=self.data_producer)


if __name__ == '__main__':
    dashboard = MonitorDashboard().run()