import sys
import tkinter as tk
import tkinter.ttk as ttk

from ui.all_processes_ui import AllProcesses


def create_notebook(parent):
    """Create ttk notebook"""
    notebook = ttk.Notebook(parent)
    notebook.pack(fill='both', pady=3, padx=3, expand=True)
    notebook.configure(width=1024, height=768)
    frame1 = ttk.Frame(notebook, width=1024, height=768)
    frame1.grid(column=0, row=0, sticky='nsew')
    notebook.add(frame1, text='All Processes')
    processes_container = ttk.Frame(frame1, width=1024, height=700, padding=5, relief='sunken')
    AllProcesses(processes_container, notebook)


# TODO create functions for menu options
def create_menubar(parent) -> tk.Menu:
    """Create menubar for main window"""
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


def destroyer():
    """Destroy all processes associated with app on close."""
    sys.exit()


class MainUi:
    """Create main window and start loop."""
    root = tk.Tk()
    root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}')
    root.title('OS Monitoring Tool')
    root.protocol("WM_DELETE_WINDOW", destroyer)
    menubar = create_menubar(root)
    create_notebook(root)
    root.configure(menu=menubar)
    root.mainloop()

