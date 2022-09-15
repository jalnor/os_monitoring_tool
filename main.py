import time
from threading import Thread

from ui import main_ui
from db.computer_processes import ComputerProcesses


def start_ui():
    return main_ui.MainUi()


def start_daemon():
    cp = ComputerProcesses()
    start_time = round(time.time())
    while True:
        if (round(time.time()) - start_time) % 10 == 0:
            cp()


if __name__ == "__main__":
    # Create a daemon thread to run ComputerProcesses
    t = Thread(target=start_daemon)
    t.daemon = True
    t.start()

    if t.is_alive():
        my_ui = start_ui()
