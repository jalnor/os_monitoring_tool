import io
import os
import platform
import subprocess
from subprocess import Popen
from time import sleep
from dotenv import load_dotenv

load_dotenv()


def start_ui():
    from ui import main_ui
    main_ui.MainUi()


if __name__ == "__main__":
    os_system = os.name
    os_platform_name = platform.system()
    if os_system == 'nt':
        print('Running file in Windows!')
        new_process = Popen(['python', '-m', 'db.computer_processes'])
    elif os_system == 'posix':
        new_process = Popen(['python', '-m', 'db.computer_processes'])
    elif os_system == 'nix':
        Popen('xdg-open location')

    if new_process:
        sleep(2)
        start_ui()




