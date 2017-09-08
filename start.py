from multiprocessing import Process, Pipe

from data.background_data_fetcher import fetch_gains_loop
from ui.dashboard import Dashboard

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

    dashboard = Dashboard(data_producer=parent_conn).run()
