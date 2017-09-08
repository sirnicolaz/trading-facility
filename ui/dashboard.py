import npyscreen
from ui.status import CoinsStatus
from ui.strategy import StrategyIndicatorsForm

class Dashboard(npyscreen.NPSAppManaged):
    keypress_timeout_default = 10

    def __init__(self, data_producer, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)
        self.data_producer = data_producer

    def onStart(self):
        self.addForm('MAIN', CoinsStatus, data_producer=self.data_producer,
                     name='Coin status dashboard', lines=1, minimum_lines=1, columns=0, editable=False)
        self.addForm('SECOND', StrategyIndicatorsForm, lines=2, minimum_lines=1, columns=0, name='Strategies', editable=False)


if __name__ == '__main__':
    dashboard = Dashboard().run()