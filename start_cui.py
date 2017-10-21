from multiprocessing import Process, Pipe
from ui.status_dashboard import StatusDashboard
from workers.gains_worker import fetch_gains_loop
from workers.coins_status_worker import fetch_coins_status_loop
from workers.order_maker_worker import make_order_loop


def run():
    parent_conn, child_conn = Pipe()
    p = Process(target=fetch_coins_status_loop, args=(child_conn,))
    p.start()

    gain_worker_parent_conn, gain_worker_child_conn = Pipe()
    mp = Process(target=fetch_gains_loop, args=(gain_worker_child_conn,))
    mp.start()

    order_maker_worker_parent_conn, order_maker_worker_child_conn = Pipe()
    op = Process(target=make_order_loop, args=(order_maker_worker_child_conn,))
    op.start()

    StatusDashboard(data_producer=parent_conn,
                    order_maker_worker_pipe=order_maker_worker_parent_conn,
                    gains_worker_pipe=gain_worker_parent_conn).run()

if __name__ == '__main__':
    run()