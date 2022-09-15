import os
import platform
from subprocess import Popen


def start_ui():
    from ui import main_ui
    main_ui.MainUi()


if __name__ == "__main__":
    os_system = os.name
    os_platform_name = platform.system()
    if os_system == 'nt':
        print('Running file in Windows!')
        # os.startfile(r'C:\Users\hal90\Documents\PyBites_PDM\os_monitoring_tool\db\computer_processes.py', 'python.exe')
        new_process = Popen(r'python C:\Users\hal90\Documents\PyBites_PDM\os_monitoring_tool\db\computer_processes.py')
        print(new_process)
    # elif os_system == 'unix':
    #     Popen('open', '')

    start_ui()




