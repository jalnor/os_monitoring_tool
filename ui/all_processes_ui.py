'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
Obtained from StackOverflow @https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
and was originally taken from @https://www.daniweb.com/programming/software-development/threads/350266/creating-table-in-python
'''
from datetime import datetime as dt, timedelta
import os
import platform
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

from tkhtmlview import HTMLLabel
import matplotlib.pyplot as plt

from db import my_db
from db.web_data import WebData
from db.graphs import Graph
from db.pybites_timer import timing


WAIT_TIME = 5000


def constant_main_tab_headers():
    return 'ID', 'Name', 'Status', 'PID', 'Start Time', 'Capture Time'


def constant_secondary_tab_headers():
    return 'PID', 'Status', 'Start Time', 'Capture Time'


def get_web_data(selection) -> str:
    return WebData.get_web_data(WebData, selection[0][1])


# TODO update this functions sorting
def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    # if data.isnumeric():
    #     data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))


class AllProcesses(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, processes_container, notebook_parent):
        self.os_name = os.name
        self.tree = None
        self.processes_container = processes_container
        self.parent = notebook_parent
        self.processes = []
        self._setup_widgets()
        self._build_tree()
        self.db = my_db.MyDb()
        self.refresh_data()
        self.style = ttk.Style()
        self.select_os_theme()

    def select_os_theme(self):
        # Check which style to apply, WILL ADD MORE LATER AND THESE MAY NEED ADJUSTING
        os_platform = platform.system()
        if os_platform == 'Windows':
            if self.os_name == 'nt':
                self.style.theme_use('winnative')
        elif os_platform == 'MacOS':
            self.style.theme_use('aqua')

    def _setup_widgets(self):
        information = """click on header to sort by that column
to change width of column drag boundary
        """
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
                        padding=(10, 2, 10, 6), text=information)
        msg.pack(fill='x')
        self.processes_container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=constant_main_tab_headers(), show="headings")
        self.tree.bind("<<TreeviewSelect>>", self.open_in_new_tab)
        self.parent.bind("<<select>>", self.on_change_tab)
        vsb = ttk.Scrollbar(orient="vertical",
                            command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.processes_container)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.processes_container)
        self.processes_container.grid_columnconfigure(0, weight=1)
        self.processes_container.grid_rowconfigure(0, weight=1)

    # @timing
    def _build_tree(self):
        for col in constant_main_tab_headers():
            self.tree.heading(col, text=col.title(), command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.adjust_column_headers(self.tree, col)

        for item in self.processes:
            if item[0]:
                self.tree.insert('', 'end', values=item)
                self.adjust_column_width(self.tree, constant_main_tab_headers(), item)

    def adjust_column_headers(self, tree, item):
        tree.column(item, width=tkFont.Font().measure(item.title()))

    def adjust_column_width(self, tree, headers, item):
        # adjust column's width if necessary to fit each value
        for ix, val in enumerate(item):
            if val is not None:
                col_w = tkFont.Font().measure(val)
            if tree.column(headers[ix], width=None) < col_w:
                tree.column(headers[ix], width=col_w)

    # @timing
    def refresh_data(self):
        # TODO get sorted state and maintain it after refresh
        # Get new processes from db
        self.processes = self.db.get_all_processes()
        self.processes.sort(key=lambda x: x[5], reverse=True)

        # Delete existing values and replace them when tree is rebuilt
        if self.tree.get_children():
            for item in self.tree.get_children():
                self.tree.delete(item)

        db_ids = [process[0] for process in self.processes]
        if db_ids:
            self._build_tree()
        # Call the function after five seconds to refresh data
        self.processes_container.after(WAIT_TIME, self.refresh_data)

    # Change focus to the new tab
    # @timing
    def on_change_tab(self, proc_tab):
        self.parent.select(proc_tab)

    # @timing
    def close_current_tab(self, fig):
        plt.close(fig)
        self.parent.forget("current")

    @timing
    def open_in_new_tab(self, event):
        result = event.widget
        graph = Graph(figsize=(1, 2), layout='constrained', dpi=100)
        # fig, ax = plt.subplots(figsize=(8, 3), layout='constrained', dpi=100)
        # selection is now a list of the values from process
        selection = [result.item(item)['values'] for item in result.selection()]

        yesterday = dt.now() - timedelta(hours=24)
        hour = dt.now() - timedelta(hours=1)
        print('Time difference: ', (dt.now() - hour))
        # Get data relating to process
        """ Not working correctly """
        graph.data_for_process = self.db.get_process_data(selection[0][0], hour, dt.now())
        graph.data_for_process.sort(key=lambda x: x[3], reverse=True)
        print('Length of data: ', len(graph.data_for_process))
        frame2 = ttk.Frame(self.parent, width=1024, height=768)
        frame2.grid(column=0, row=0, sticky='nsew')
        self.parent.add(frame2, text=selection[0][1])
        self.on_change_tab(frame2)

        process_container = ttk.Frame(frame2, width=1024, height=768, padding=5, relief='sunken')
        process_container.grid(column=0, row=0, sticky='nsew')
        # Button and headings for top sections
        close_button = ttk.Button(process_container, text="Close", command=lambda: self.close_current_tab(graph.fig))
        close_button.grid(column=0, row=0, sticky='w')
        ttk.Label(process_container, text="Current Process", padding=2).grid(column=1, row=0, sticky='w')
        ttk.Label(process_container, text="Process History", padding=2).grid(column=2, row=0, sticky='w')

        # Column 1 frame with current process name and id
        name_frame = ttk.Frame(process_container, width=150, height=350,
                               padding=5, borderwidth=5, relief='flat')
        name_frame.grid(column=1, row=1, sticky='nsew')

        ttk.Label(name_frame, text=selection[0][0], justify='center').grid(column=1, row=1)
        ttk.Label(name_frame, text=selection[0][1], justify='center').grid(column=1, row=2)

        # Create the data frame and tree to display logs
        data_frame = ttk.Frame(process_container, width=700, height=350, padding=5, borderwidth=5, relief='flat')
        data_frame.grid(column=2, columnspan=4, row=1, sticky='nsew')
        data_tree = ttk.Treeview(data_frame, columns=constant_secondary_tab_headers(), show='headings')
        data_tree.grid(column=0, row=0, in_=data_frame)

        data_frame.grid_columnconfigure(0, weight=1)
        data_frame.grid_rowconfigure(0, weight=1)

        for header in constant_secondary_tab_headers():
            data_tree.heading(header, text=header.title(),
                              command=lambda c=header: sortby(data_tree, c, 0))
            self.adjust_column_headers(data_tree, header)

        for data in graph.data_for_process:
            data_tree.insert('', 'end', values=data)
            self.adjust_column_width(data_tree, constant_secondary_tab_headers(), data)

        graph_frame = ttk.Frame(process_container, width=1000, height=150, padding=5, borderwidth=5, relief='sunken')
        graph_frame.grid(column=0, columnspan=6, row=5, sticky='nsew')

        graph.list_of_statuses = [(1 if dt[1] == 'running' else 0) for dt in graph.data_for_process]

        graph.set_major_stuff()
        canvas = graph.set_frame(graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        text_frame = ttk.Frame(process_container, width=1900, height=150, padding=5, borderwidth=5, relief='sunken')
        text_frame.grid(column=0, row=6, sticky='nsew')

        text_canvas = ttk.Frame(text_frame, width=875, height=150, padding=2, borderwidth=2, relief='sunken')
        text_canvas.grid(column=0, row=0, sticky='nsew')

        web_data = WebData.get_web_data(WebData, process_name=selection[0][1], os_name=self.os_name)
        web_data = web_data.splitlines('\n')

        main_label = tk.Text(text_canvas, text=''.join(web_data[:-1]), padding=2, wraplength=950)
        main_label.grid(column=0, row=0)

        vsb = ttk.Scrollbar(orient="vertical", command=main_label.yview())
        hsb = ttk.Scrollbar(orient="horizontal", command=main_label.xview())
        vsb.grid(column=1, row=0, sticky='ns', in_=text_canvas)
        hsb.grid(column=1, row=1, sticky='ew', in_=text_canvas)
        my_label = HTMLLabel(text_canvas, html=''.join(web_data[-1:]))
        my_label.grid(column=0, row=1)

        process_container.pack(fill="both", expand=True)
        for child in process_container.winfo_children():
            child.grid_configure(padx=5, pady=5)
