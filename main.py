import os
import platform
from subprocess import Popen
from time import sleep
from dotenv import load_dotenv

load_dotenv()


def start_ui():
    from ui import main_ui
    main_ui.MainUi()


if __name__ == "__main__":
    os_system = os.name
    # ms_platform_name = platform.system()
    # mac_platform_name = platform.uname()
    # print('Windows ', ms_platform_name)
    print(f"{os_system=}")  # f-string debugging trick :)

    computer_processes_cmd = ['python', "-m", "db.computer_processes"]
    if os_system == 'nt':
        print('Running file in Windows!')
        new_process = Popen(computer_processes_cmd)
    elif os_system == 'posix':
        print('On a Mac')
        new_process = Popen(computer_processes_cmd)
    elif os_system == 'nix':
        print('On other Unix system')
        # TODO: do we need to assign to new_process here as well?
        Popen('xdg-open location')

    if new_process:
        sleep(3)
        start_ui()
