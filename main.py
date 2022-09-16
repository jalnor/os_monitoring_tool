import io
import os
import platform
import subprocess
from subprocess import Popen


list_of_processes = []


def start_ui():
    from ui import main_ui
    main_ui.MainUi()


if __name__ == "__main__":
    os_system = os.name
    os_platform_name = platform.system()
    if os_system == 'nt':
        print('Running file in Windows!')
        new_process = Popen(r'python C:\Users\hal90\Documents\PyBites_PDM\os_monitoring_tool\db\computer_processes.py')
        print(list_of_processes)
    elif os_system == 'unix':
        Popen('python location-of-file')
    elif os_system == 'nix':
        Popen('xdg-open location')

    start_ui()




