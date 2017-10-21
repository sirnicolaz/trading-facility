from multiprocessing import Process, Queue
from ui.monitor_dashboard import MonitorDashboard
from workers.monitor_worker import fetch_indicators


def run():
    monitor_worker_queue = Queue()
    mp = Process(target=fetch_indicators, args=(monitor_worker_queue,))
    mp.start()

    MonitorDashboard(data_producer=monitor_worker_queue).run()

if __name__ == '__main__':
    run()