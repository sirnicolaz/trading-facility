import sys
import importlib
import ta_trackers.looper as looper
from threading import Thread
import signal
from time import sleep

if __name__ == "__main__":
    trackers = []
    for tracker in sys.argv[1:]:
        name = "ta_trackers." + tracker
        mod = importlib.import_module(name)

        t = Thread(target=looper.run_loop, args=(mod.run,))
        t.setDaemon(True)
        t.start()
        trackers.append(t)

    print("trackers are running in the background. Ctrl-C to quit all.")
    [tracker.join() for tracker in trackers]
    print("all trackers exited.")

