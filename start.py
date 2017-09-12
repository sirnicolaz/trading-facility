from multiprocessing import Process, Pipe
from ui.dashboard import Dashboard
from workers.gains_worker import fetch_gains_loop, calculate_gains
from workers.coins_status_worker import fetch_coins_status_loop
from workers.coins_status_worker import get_aggregated_data

if __name__ == '__main__':
    #network_queue = Queue()
    #request_handler.set_queue(queue=network_queue)
    #keep_alive_loop_process = Process(target=keep_alive_loop, args=(network_queue,))
    #request_handling_loop_process = Process(target=hidden_api_manager.request_handling_loop, args=(network_queue))
    #keep_alive_loop_process.start()
    #request_handling_loop_process.start()
    reference_currency = "btc"

    parent_conn, child_conn = Pipe()
    p = Process(target=fetch_coins_status_loop, args=(child_conn, reference_currency))
    p.start()

    manager_parent_conn, manager_child_conn = Pipe()
    mp = Process(target=fetch_gains_loop, args=(manager_child_conn, reference_currency))
    mp.start()

    dashboard = Dashboard(reference_currency=reference_currency,
                          data_producer=parent_conn, gains_worker_pipe=manager_parent_conn).run()
