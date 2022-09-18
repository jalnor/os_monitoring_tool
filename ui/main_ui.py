import tkinter as tk
import tkinter.ttk as ttk

from ui.all_processes_ui import AllProcesses


def create_notebook(parent):
    n = ttk.Notebook(parent)
    n.pack(pady=3, padx=3, expand=True)
    n.configure(width=1024, height=768)
    f1 = ttk.Frame(n, width=1024, height=768)
    f1.grid(column=0, row=0, sticky='nsew')
    n.add(f1, text='All Processes')
    processes_container = ttk.Frame(f1, width=1024, height=700, padding=5, relief='sunken')
    AllProcesses(processes_container, n)


# TODO create functions for menu options
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


class MainUi:
    root = tk.Tk()
    root.geometry('1024x768')
    root.title('OS Monitoring Tool')
    menubar = create_menubar(root)
    create_notebook(root)
    root.configure(menu=menubar)
    root.mainloop()

