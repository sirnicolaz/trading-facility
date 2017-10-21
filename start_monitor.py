from multiprocessing import Process, Queue
from ui.monitor_dashboard import MonitorDashboard
from workers.monitor_worker import fetch_indicators


if __name__ == '__main__':
    monitor_worker_queue = Queue()
    mp = Process(target=fetch_indicators, args=(monitor_worker_queue,))
    mp.start()

    dashboard = MonitorDashboard(data_producer=monitor_worker_queue).run()
