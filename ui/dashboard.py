import npyscreen
from ui.status import CoinsStatus
from ui.strategy import StrategyIndicatorsForm
from ui.manage_coin import ManageCoin


class Dashboard(npyscreen.NPSAppManaged):
    keypress_timeout_default = 10

    def __init__(self, data_producer, gains_worker_pipe, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)
        self.data_producer = data_producer
        self.gains_worker_pipe = gains_worker_pipe

    def onStart(self):
        self.addForm('MAIN', CoinsStatus , data_producer=self.data_producer)
        self.addForm('MANAGECOINFM', ManageCoin, gains_worker_pipe=self.gains_worker_pipe)
        #self.addForm('STRATEGYFM', StrategyIndicatorsForm, lines=2, minimum_lines=1, columns=0, name='Strategies', editable=False)


if __name__ == '__main__':
    dashboard = Dashboard().run()