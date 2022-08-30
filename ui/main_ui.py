import tkinter as tk
import tkinter.ttk as ttk

from ui.all_processes_ui import AllProcesses


def create_notebook(parent):
    n = ttk.Notebook(parent)
    n.pack(pady=10, expand=True)
    f1 = ttk.Frame(n, width=1000, height=480)
    f2 = ttk.Frame(n, width=1000, height=480)
    n.add(f1, text='All Processes')
    n.add(f2, text='Process')
    all_processes_frame = ttk.Frame(f1, width=780, height=500, relief='sunken')
    AllProcesses(all_processes_frame)


def create_menubar(parent):
    win = tk.Toplevel(parent)
    menubar = tk.Menu(win)
    win['menu'] = menubar
    # Add menus
    menu_file = tk.Menu(menubar)
    menu_edit = tk.Menu(menubar)
    menubar.add_cascade(menu=menu_file, label='File')
    menubar.add_cascade(menu=menu_edit, label='Edit')
    # Add additional menus
    menu_file.add_command(label='New', command='newFile')
    menu_file.add_command(label='Open...', command='openFile')
    menu_file.add_command(label='Close', command='closeFile')


class MainUi:
    root = tk.Tk()
    root.option_add('*tearOFF', False)
    root.geometry('1000x550')
    root.title('OS Monitoring Tool')

    create_menubar(root)

    create_notebook(root)
    root.mainloop()

