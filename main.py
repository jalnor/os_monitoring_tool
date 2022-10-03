import os
from subprocess import Popen
from time import sleep
from dotenv import load_dotenv

load_dotenv()


def start_ui():
    from ui import main_ui
    main_ui.MainUi()


if __name__ == "__main__":
    os_system = os.name
    if os_system == 'nt' or os_system == 'posix':
        new_process = Popen(['python', '-m', 'db.computer_processes'])

    if new_process:
        sleep(2)
        start_ui()




