from multiprocessing import Process, Pipe
from data.background_data_fetcher import fetch_gains_loop
from ui.dashboard import Dashboard


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()

    p = Process(target=fetch_gains_loop, args=(child_conn,))
    p.start()

    dashboard = Dashboard(data_producer=parent_conn).run()
