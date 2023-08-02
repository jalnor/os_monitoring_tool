import os
from subprocess import Popen
from time import sleep

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def start_ui():
    from src.ui import main_ui
    main_ui.MainUi()


if __name__ == "__main__":
    os_system = os.name
    if os_system in ('nt', 'posix'):
        new_process = Popen(['python', '-m', Path('db.computer_processes')])

    if not new_process == 'undefined':
        sleep(2)
        start_ui()

