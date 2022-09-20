'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
Obtained from StackOverflow @https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
and was originally taken from @https://www.daniweb.com/programming/software-development/threads/350266/creating-table-in-python
'''
import os
import platform
import time
import tkinter.font as tkFont
import tkinter.ttk as ttk

from db import my_db
from db.web_data import WebData


def constant_main_tab_headers():
    return 'ID', 'Name', 'Status', 'PID', 'Start Time', 'Capture Time'


def constant_secondary_tab_headers():
    return 'PID', 'Status', 'Start Time', 'Capture Time'


class AllProcesses(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, processes_container, notebook_parent):
        # Get the os info to apply up-to-date styling
        os_name = os.name
        os_platform = platform.system()
        # Please check this print out to see if naming in 'if' statement below is correct
        print(os_name, ':', os_platform)
        self.tree = None
        self.processes_container = processes_container
        self.parent = notebook_parent
        self.processes = []
        self._setup_widgets()
        self._build_tree()
        self.db = my_db.MyDb()
        # self.cp = OSProcesses()
        self.refresh_data()
        self.style = ttk.Style()
        # Check which style to apply, WILL ADD MORE LATER AND THESE MAY NEED ADJUSTING
        if os_platform == 'Windows':
            if os_name == 'nt':
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
        hsb = ttk.Scrollbar(orient="horizontal",
                            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
                            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.processes_container)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.processes_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=self.processes_container)
        self.processes_container.grid_columnconfigure(0, weight=1)
        self.processes_container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col in constant_main_tab_headers():
            self.tree.heading(col, text=col.title(),
                              command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.adjust_column_headers(self.tree, col)
            # self.tree.column(col,
            #                  width=tkFont.Font().measure(col.title()))

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

    def refresh_data(self):
        start_time = time.time()
        # print("Starting refresh...", start_time)

        # Get new processes from db
        self.processes = self.db.get_all_processes()
        self.processes.sort(key=lambda x: x[5], reverse=True)

        # print("Retrieved new data from db...", time.time() - start_time)
        # Delete existing values and replace them when tree is rebuilt
        if self.tree.get_children():
            for item in self.tree.get_children():
                self.tree.delete(item)
        # print("Deleted tree values...", time.time() - start_time, 'length of new list: ', len(self.processes))
        db_ids = [process[0] for process in self.processes]
        if db_ids:
            self._build_tree()
        # print("Rebuilt tree...", time.time() - start_time)
        # Call the function after one minute to refresh data
        self.processes_container.after(5000, self.refresh_data)

    # Change focus to the new tab
    def on_change_tab(self, proc_tab):
        self.parent.select(proc_tab)

    def close_current_tab(self):
        self.parent.forget("current")

    def open_in_new_tab(self, event):
        result = event.widget
        # selection is now a list of the values from process
        selection = [result.item(item)['values'] for item in result.selection()]
        print("It's Working! ", selection[0][0])

        # Get data relating to process
        data_for_process = self.db.get_process_data(selection[0][0])
        data_for_process.sort(key=lambda x: x[3], reverse=True)

        f2 = ttk.Frame(self.parent, width=1024, height=768)
        f2.grid(column=0, row=0, sticky='nsew')
        self.parent.add(f2, text="Process")
        self.on_change_tab(f2)

        process_container = ttk.Frame(f2, width=1024, height=768, padding=5, relief='sunken')
        process_container.grid(column=0, row=0, sticky='nsew')
        # Button and headings for top sections
        close_button = ttk.Button(process_container, text="Close", command=self.close_current_tab)
        close_button.grid(column=0, row=0, sticky='w')
        ttk.Label(process_container, text="Current Process", padding=2).grid(column=1, row=0, sticky='w')
        ttk.Label(process_container, text="Process History", padding=2).grid(column=2, row=0, sticky='w')

        # Column 1 frame with current process name and id
        name_frame = ttk.Frame(process_container, width=150, height=350,
                               padding=5, borderwidth=5, relief='flat')
        name_frame.grid(column=1, row=1, sticky='nw')

        ttk.Label(name_frame, text=selection[0][0], justify='center').grid(column=1, row=1)
        ttk.Label(name_frame, text=selection[0][1], justify='center').grid(column=1, row=2)

        # Create the data frame and tree to display logs
        data_frame = ttk.Frame(process_container, width=700, height=350, padding=5, borderwidth=5, relief='flat')
        data_frame.grid(column=2, columnspan=4, row=1, sticky='nw')
        data_tree = ttk.Treeview(data_frame, columns=constant_secondary_tab_headers(), show='headings')
        # data_vsb = ttk.Scrollbar(orient='vertical', command=data_tree.yview())
        # data_vsb.grid(column=1, row=0, sticky='ns', in_=data_frame)
        # data_hsb = ttk.Scrollbar(orient='horizontal', command=data_tree.xview())
        # data_hsb.grid(column=0, row=1, sticky='ew', in_=data_frame)
        # data_tree.configure(yscrollcommand=data_vsb, xscrollcommand=data_hsb)
        data_tree.grid(column=0, row=0, in_=data_frame)
        data_frame.grid_columnconfigure(0, weight=1)
        data_frame.grid_rowconfigure(0, weight=1)

        for header in constant_secondary_tab_headers():
            data_tree.heading(header, text=header.title(),
                              command=lambda c=header: sortby(self.tree, c, 0))
            self.adjust_column_headers(data_tree, header)

        for data in data_for_process:
            data_tree.insert('', 'end', values=data)
            self.adjust_column_width(data_tree, constant_secondary_tab_headers(), data)

        text_frame = ttk.Frame(process_container, width=900, height=150, padding=5, borderwidth=5, relief='sunken')
        text_frame.grid(column=0, columnspan=6, row=5, rowspan=10, sticky='sw')

        ttk.Label(text_frame, text=WebData.get_web_data(WebData, selection[0][1]), padding=10, wraplength=950)\
            .grid(column=1, columnspan=10, row=1, rowspan=10)

        process_container.pack(fill="both", expand=True)
        for child in process_container.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # TODO Add in a canvas to create graphs of the data presented


# I am going to update this as it does not work as I would like it to!!!
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
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
                                                     int(not descending)))
