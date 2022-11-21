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
from db import web_data as wd
from db.graphs import Graph
from db.pybites_timer import timing


def constant_main_tab_headers():
    """Define main window header names"""
    return 'ID', 'Name', 'Status', 'PID', 'Start Time', 'Capture Time'


def constant_secondary_tab_headers():
    """Define process tab header names"""
    return 'PID', 'Status', 'Start Time', 'Capture Time'


def adjust_column_width(tree, headers, item):
    """Adjust column widths"""
    col_w = 8
    for ix, val in enumerate(item):
        if val is not None:
            col_w = tkFont.Font().measure(val)
        if tree.column(headers[ix], width=None) < col_w:
            tree.column(headers[ix], width=col_w)


def adjust_column_headers(tree, item):
    tree.column(item, width=tkFont.Font().measure(item.title()))


class AllProcesses(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, processes_container, notebook_parent):
        self.os_name = os.name
        self.tree = None
        self.sorted: list = [self.tree, 'Capture Time', 1]
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
        """Set the style of the widgets based on user os."""
        os_platform = platform.system()
        if os_platform == 'Windows':
            if self.os_name == 'nt':
                self.style.theme_use('winnative')
        elif os_platform == 'MacOS':
            self.style.theme_use('aqua')

    def _setup_widgets(self):
        """Set up the components of the notebook tab."""
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
        """Build the ttk.treeview setting columns and adding data."""
        for col in constant_main_tab_headers():
            self.tree.heading(col, text=col.title(), command=lambda c=col: self.sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            adjust_column_headers(self.tree, col)

        for item in self.processes:
            if item[0]:
                self.tree.insert('', 'end', values=item)
                adjust_column_width(self.tree, constant_main_tab_headers(), item)

    # TODO update this functions sorting
    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        data = [(tree.set(child, col), child)
                for child in tree.get_children('')]
        # now sort the data in place
        data.sort(reverse=descending)
        for index, item in enumerate(data):
            tree.move(item[1], '', index)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, int(not descending)))
        # Add sorted column to sorted tuple
        self.sorted = [tree, col, descending]

    def delete_tree_items(self):
        """Delete existing values"""
        if self.tree.get_children():
            for item in self.tree.get_children():
                self.tree.delete(item)

    def rebuild_tree(self):
        """Rebuild tree with new process list."""
        db_ids = [process[0] for process in self.processes]
        if db_ids:
            self._build_tree()

    # @timing
    def refresh_data(self):
        """Fetch latest data from database."""
        wait_time = 5000

        self.processes = self.db.get_all_processes()

        self.delete_tree_items()
        self.rebuild_tree()

        self.sorted[0] = self.tree

        if self.tree is not None:
            self.sortby(self.sorted[0], self.sorted[1], self.sorted[2])
        # Call the function after five seconds to refresh data
        self.processes_container.after(wait_time, self.refresh_data)

    # @timing
    def on_change_tab(self, proc_tab):
        """Change to new tab on creation.

        Keyword arguments:
        proc_tab -- the newly created tab
        """
        self.parent.select(proc_tab)

    # @timing
    def close_current_tab(self, fig):
        """Close the current tab.

        Keyword arguments:
        fig -- the matplotlib graph
        """
        plt.close(fig)
        self.parent.forget("current")

    @timing
    def open_in_new_tab(self, event):
        result = event.widget
        # selection is now a list of the values from process
        selection = [result.item(item)['values'] for item in result.selection()]
        if selection:  # Fixes console error on refresh
            frame2 = ttk.Frame(self.parent, width=1024, height=768)
            frame2.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
            frame2.grid_columnconfigure(0, weight=1)
            self.parent.add(frame2, text=selection[0][1])
            self.on_change_tab(frame2)

            process_container = ttk.Frame(frame2, width=1024, height=768, padding=5, relief='sunken')

            process_container.grid(column=0, row=0, sticky='nsew')
            process_container.grid_columnconfigure(0, weight=1)

            # Button and headings for top sections columns 1, 2, 3 respectively & row 0
            close_button = ttk.Button(process_container, text="Close",
                                      command=lambda: self.close_current_tab(graph.fig))
            close_button.grid(column=0, row=0, sticky='w')
            ttk.Label(process_container, text="Current Process", padding=2).grid(column=1, row=0, sticky='w')
            ttk.Label(process_container, text="Process History", padding=2).grid(column=2, row=0, sticky='w')

            graph = Graph(figsize=(8, 3), layout='constrained', dpi=100)

            # TODO implement combobox selection for time period, make graph zoomable, seekable
            yesterday = dt.now() - timedelta(hours=24)
            hour = dt.now() - timedelta(hours=1)
            print('Time difference: ', (dt.now() - hour))
            # Get data relating to process
            """ Not working correctly """
            graph.data_for_process = self.db.get_process_data(selection[0][0], hour, dt.now())

            # Column 0, row 1, Combo boxes for graph selection, Graph starts at past hour
            graph_selection_frame = ttk.Frame(process_container, width=200, height=250, padding=5)
            print(graph_selection_frame['style'], ' ', graph_selection_frame.winfo_class())
            graph_selection_frame.grid(column=0, row=1, sticky='nsew')
            graph_selection_frame.grid_columnconfigure(0, weight=1)
            graph_selection_frame.grid_rowconfigure(0, weight=1)
            graph_selection_frame['style'] = 'Graph.TFrame'
            graph_selection_style = ttk.Style()
            graph_selection_style.configure("Graph.TFrame", background="lightblue")
            selected = tk.StringVar()
            graph_combobox = ttk.Combobox(graph_selection_frame, width=10, textvariable=selected)
            graph_combobox['values'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
            graph_combobox.grid(column=0, row=0, pady=5, padx=5)
            graph_combobox.current(newindex=1)

            # Column 1, row 1 frame with current process name and id
            name_frame = ttk.Frame(process_container, width=150, height=250,
                                   padding=5, borderwidth=5, relief='flat')
            name_frame.grid(column=1, row=1, sticky='ne')
            name_frame.grid_columnconfigure(0, weight=1)

            ttk.Label(name_frame, text=selection[0][0], justify='center').grid(column=1, row=1, sticky='nsew')
            ttk.Label(name_frame, text=selection[0][1], justify='center').grid(column=1, row=2, sticky='nsew')

            # Create the data frame and tree to display logs
            data_frame = ttk.Frame(process_container, width=700, height=250, padding=5, borderwidth=5, relief='flat')
            data_frame.grid(column=2, columnspan=4, row=1, sticky='nsew')
            data_frame.grid_columnconfigure(0, weight=1)
            data_frame.grid_rowconfigure(0, weight=1)
            data_tree = ttk.Treeview(data_frame, columns=constant_secondary_tab_headers(), show='headings')
            data_tree.grid(column=0, row=0, in_=data_frame)

            data_frame.grid_columnconfigure(0, weight=1)
            data_frame.grid_rowconfigure(0, weight=1)

            for header in constant_secondary_tab_headers():
                data_tree.heading(header, text=header.title(),
                                  command=lambda c=header: self.sortby(data_tree, c, 0))
                adjust_column_headers(data_tree, header)

            for data in graph.data_for_process:
                data_tree.insert('', 'end', values=data)
                adjust_column_width(tree=data_tree, headers=constant_secondary_tab_headers(), item=data)

            graph_frame = ttk.Frame(process_container, width=1000, height=500, padding=5, borderwidth=5,
                                    relief='sunken')

            graph_frame.grid(column=0, columnspan=6, row=5, sticky='nsew')
            graph_frame.grid_columnconfigure(0, weight=1)
            graph_frame.grid_rowconfigure(0, weight=1)
            graph.list_of_statuses = [(1 if dt[1] == 'running' else 0) for dt in graph.data_for_process]

            graph.set_major_stuff()
            canvas = graph.set_frame(graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

            text_frame = ttk.Frame(process_container, width=1900, height=150, padding=5, borderwidth=5, relief='sunken')
            text_frame.grid(column=0, columnspan=6, row=6, sticky='nsew')
            text_frame.grid_columnconfigure(0, weight=1)
            text_frame.grid_rowconfigure(0, weight=1)

            text_frame_style = ttk.Style()

            web_data = wd.get_web_data(process_name=selection[0][1], os_name=self.os_name)
            web_data = web_data.split('\\n')

            label_text = ''.join(web_data[0:-1])
            main_label = ttk.Label(text_frame, width=1000, text=label_text, padding=10, font=('Arial', 14),
                                   justify='center', wraplength=1600)
            main_label.grid(column=0, columnspan=6, row=1, in_=text_frame)
            main_label.grid_columnconfigure(0, weight=1)
            main_label['style'] = 'Webdata.TLabel'
            text_frame_style.configure('Webdata.TLabel', size=14)

            my_label = HTMLLabel(text_frame, html=''.join(web_data[-1:]).replace('\'', '').replace('"', ''))
            my_label.grid(column=0, row=2, in_=text_frame)

            process_container.pack(fill="both", expand=True)
            for child in process_container.winfo_children():
                child.grid_configure(padx=5, pady=5)
