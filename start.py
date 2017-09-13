from multiprocessing import Process, Pipe
from ui.dashboard import Dashboard
from workers.gains_worker import fetch_gains_loop
from workers.coins_status_worker import fetch_coins_status_loop

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=fetch_coins_status_loop, args=(child_conn,))
    p.start()

    manager_parent_conn, manager_child_conn = Pipe()
    mp = Process(target=fetch_gains_loop, args=(manager_child_conn,))
    mp.start()

    dashboard = Dashboard(data_producer=parent_conn, gains_worker_pipe=manager_parent_conn).run()
