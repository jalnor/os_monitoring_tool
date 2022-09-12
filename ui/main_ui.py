import time
import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread

from db.computer_processes import ComputerProcesses
from ui.all_processes_ui import AllProcesses


def create_notebook(parent):
    n = ttk.Notebook(parent)
    n.pack(pady=10, expand=True)
    f1 = ttk.Frame(n, width=1000, height=450)
    f2 = ttk.Frame(n, width=1000, height=450)
    n.add(f1, text='All Processes')
    n.add(f2, text='Process')
    process_container = ttk.Frame(f1, width=780, height=450, relief='sunken')
    AllProcesses(process_container)


def create_menubar(parent) -> tk.Menu:
    menubar = tk.Menu(parent)
    # Add menus
    menu_file = tk.Menu(menubar, tearoff=0)
    menu_edit = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(menu=menu_file, label='File')
    menubar.add_cascade(menu=menu_edit, label='Edit')
    # Add additional menus
    menu_file.add_command(label='New', command='newFile')
    menu_file.add_command(label='Open...', command='openFile')
    menu_file.add_command(label='Close', command='closeFile')

    return menubar


def start_daemon():
    cp = ComputerProcesses()
    start_time = round(time.time())
    while True:
        if (round(time.time()) - start_time) % 30 == 0:
            print('Update')
            cp()


class MainUi:
    root = tk.Tk()
    root.geometry('1000x550')
    root.title('OS Monitoring Tool')
    menubar = create_menubar(root)
    create_notebook(root)
    # Create a daemon thread to run ComputerProcess
    t = Thread(target=start_daemon)
    t.daemon = True
    t.start()
    # Checking status to do something with maybe
    print("Thread is running: ", t.is_alive())
    print(t.native_id)

    root.configure(menu=menubar)
    root.mainloop()

