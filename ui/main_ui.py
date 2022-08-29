from model.process import get_processes
from ui.all_processes_ui import AllProcesses
try:
    import Tkinter as tk
    import ttk
except:
    import tkinter as tk
    import tkinter.ttk as ttk


def create_notebook(parent):
    n = ttk.Notebook(parent)
    n.pack(pady=10, expand=True)
    f1 = ttk.Frame(n, width=400, height=280)
    f2 = ttk.Frame(n, width=400, height=280)
    n.add(f1, text='All Processes')
    n.add(f2, text='Process')
    all_processes_frame = ttk.Frame(f1, width=380, height=400, relief='sunken')
    AllProcesses(all_processes_frame)


class MainUi:
    root = tk.Tk()
    root.geometry('400x300')
    root.title('OS Monitoring Tool')
    bt = tk.Button(root, text="Get Processes", command=get_processes)
    create_notebook(root)
    root.mainloop()

