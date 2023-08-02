import os
from pathlib import Path
from subprocess import Popen
from time import sleep
from dotenv import load_dotenv

load_dotenv()


def start_ui(process):
    from src.ui import main_ui
    main_ui.MainUi(new_process=process)


if __name__ == "__main__":
    os_system = os.name
    if os_system in ('nt', 'posix'):
        # For installer packaging
        new_process = Popen(['computer_processes'])
        # For debugging testing
        # new_process = Popen(['python', '-m', 'db.computer_processes'])

    if new_process:
        sleep(2)
        start_ui(new_process)
