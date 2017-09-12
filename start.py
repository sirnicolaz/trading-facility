from multiprocessing import Process, Pipe
from ui.dashboard import Dashboard
from workers.order_manager import manage_order
from workers.background_data_fetcher import fetch_gains_loop

if __name__ == '__main__':
    #network_queue = Queue()
    #request_handler.set_queue(queue=network_queue)
    #keep_alive_loop_process = Process(target=keep_alive_loop, args=(network_queue,))
    #request_handling_loop_process = Process(target=hidden_api_manager.request_handling_loop, args=(network_queue))
    #keep_alive_loop_process.start()
    #request_handling_loop_process.start()
    parent_conn, child_conn = Pipe()
    p = Process(target=fetch_gains_loop, args=(child_conn,))
    p.start()

    manager_parent_conn, manager_child_conn = Pipe()
    mp = Process(target=manage_order, args=(manager_child_conn,))
    mp.start()

    dashboard = Dashboard(data_producer=parent_conn, manager_pipe=manager_parent_conn).run()
