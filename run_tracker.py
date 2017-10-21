import sys
import importlib
import ta_trackers.looper as looper
from threading import Thread


def run(trackers):
    tracker_threads = []
    for tracker in list(set(trackers)):
        name = "ta_trackers." + tracker
        mod = importlib.import_module(name)

        t = Thread(target=looper.run_loop, args=(mod.run,))
        t.setDaemon(True)
        t.start()
        tracker_threads.append(t)

    print("trackers %s are running in the background. Ctrl-C to quit all." % ", ".join(trackers))
    [tracker.join() for tracker in tracker_threads]
    print("all trackers exited.")


if __name__ == "__main__":
    run(sys.argv[1:])

