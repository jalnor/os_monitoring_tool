'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
Obtained from StackOverflow @https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
and was originally taken from @https://www.daniweb.com/programming/software-development/threads/350266/creating-table-in-python
'''
from datetime import datetime as dt, timedelta
import os
import platform
import tkinter.font as tkFont
import tkinter.ttk as ttk
import matplotlib
from tkhtmlview import HTMLLabel
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import matplotlib.dates as mdates

from db import my_db
from db.web_data import WebData
from db.pybites_timer import timing


matplotlib.use('TkAgg')


def constant_main_tab_headers():
    return 'ID', 'Name', 'Status', 'PID', 'Start Time', 'Capture Time'


def constant_secondary_tab_headers():
    return 'PID', 'Status', 'Start Time', 'Capture Time'


class AllProcesses(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, processes_container, notebook_parent):
        # Get the os info to apply up-to-date styling
        self.os_name = os.name
        os_platform = platform.system()
        # Please check this print out to see if naming in 'if' statement below is correct
        # print(self.os_name, ':', os_platform)
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
        hsb = ttk.Scrollbar(orient="horizontal",
                            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
                            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.processes_container)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.processes_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=self.processes_container)
        self.processes_container.grid_columnconfigure(0, weight=1)
        self.processes_container.grid_rowconfigure(0, weight=1)

    # @timing
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
        # TODO make wait time a variable
        self.processes_container.after(5000, self.refresh_data)

    # Change focus to the new tab
    # @timing
    def on_change_tab(self, proc_tab):
        self.parent.select(proc_tab)

    # @timing
    def close_current_tab(self, fig):
        plt.close(fig)
        self.parent.forget("current")

    # @timing
    def open_in_new_tab(self, event):
        result = event.widget
        fig, ax = plt.subplots(figsize=(8, 3), layout='constrained', dpi=100)
        # selection is now a list of the values from process
        selection = [result.item(item)['values'] for item in result.selection()]

        yesterday = dt.now() - timedelta(hours=24)
        hour = dt.now() - timedelta(hours=1)
        print('Time difference: ', (dt.now() - hour))
        # Get data relating to process
        """ Not working correctly """
        data_for_process = self.db.get_process_data(selection[0][0], hour, dt.now())
        data_for_process.sort(key=lambda x: x[3], reverse=True)
        print('Length of data: ', len(data_for_process))
        frame2 = ttk.Frame(self.parent, width=1024, height=768)
        frame2.grid(column=0, row=0, sticky='nsew')
        self.parent.add(frame2, text=selection[0][1])
        self.on_change_tab(frame2)

        process_container = ttk.Frame(frame2, width=1024, height=768, padding=5, relief='sunken')
        process_container.grid(column=0, row=0, sticky='nsew')
        # Button and headings for top sections
        close_button = ttk.Button(process_container, text="Close", command=lambda: self.close_current_tab(fig))
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

        for data in data_for_process:
            data_tree.insert('', 'end', values=data)
            self.adjust_column_width(data_tree, constant_secondary_tab_headers(), data)

        graph_frame = ttk.Frame(process_container, width=1000, height=250, padding=5, borderwidth=5, relief='sunken')
        graph_frame.grid(column=0, columnspan=6, row=5, sticky='nsew')

        list_of_statuses = [(1 if dt[1] == 'running' else 0) for dt in data_for_process]
        print(list_of_statuses)

        ax2 = ax.twiny()
        plt.xlim(xmin=0.0)
        plt.ylim(ymin=0.0)

        time_lists = []
        x_minor = [dt[2].time().strftime('%H:%M:%S') for dt in data_for_process]

        x_minor_floats = [float(x) for x in range(0, len(x_minor))]

        x_major = list(dict.fromkeys([str(dt[2]).split(' ')[0] for dt in data_for_process]))
        count = 0
        for x in x_major:
            time_lists.append(
                [y[2].time().strftime('%H:%M:%S') for y in data_for_process if str(y[2]).split(" ")[0] == x])

        x_major_locations = [0.0]
        last_x = 0
        for x in time_lists[:(len(time_lists) - 1)]:
            x_major_locations.append(len(x) + last_x + 1)
            last_x += len(x)

        ax.plot(list_of_statuses, label='Status')

        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax2.format_xdata = mdates.DateFormatter('%H:%M:%S')

        ax.set_yticks(ticks=[0.0, 1.0], labels=['Stopped', 'Running'], rotation=45)

        ax.minorticks_off()
        ax.tick_params(which='major', length=8, width=2, color='blue', labelcolor='blue', bottom=True,
                       top=False, labeltop=False, labelbottom=True, pad=40, rotation=20)
        ax.set_xticks(ticks=x_major_locations, labels=x_major, minor=False)

        ax2.minorticks_on()
        ax2.xaxis.set_minor_locator(MultipleLocator(1))
        ax2.yaxis.set_minor_locator(MultipleLocator(1))
        ax2.tick_params(axis='x', which='minor', length=4, color='red', labelcolor='red', rotation=70, bottom=True,
                        top=False, labeltop=False, labelbottom=True, labelsize=8, direction='in')
        ax2.set_xticks(ticks=x_minor_floats, labels=x_minor, minor=True)

        ax.set_title('Status')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        text_frame = ttk.Frame(process_container, width=900, height=150, padding=5, borderwidth=5, relief='sunken')
        text_frame.grid(column=0, columnspan=6, row=15, rowspan=5, sticky='nsew')
        # p = ttk.Progressbar(text_frame, orient='horizontal', length=200, mode='determinate')
        # p.start()

        web_data = WebData.get_web_data(WebData, process_name=selection[0][1], os_name=self.os_name)
        web_data = web_data.split('\n')
        # p.stop()
        print('Web data: ', web_data[-1:])
        main_label = ttk.Label(text_frame, text=''.join(web_data[:-1]), padding=2, wraplength=950)
        main_label.grid(column=0, row=0)
        # vsb = ttk.Scrollbar(orient="vertical")
        # hsb = ttk.Scrollbar(orient="horizontal")
        # vsb.grid(column=1, row=0, sticky='ns', in_=text_frame)
        # hsb.grid(column=1, row=10, columnspan=10, sticky='ews', in_=text_frame)
        my_label = HTMLLabel(text_frame, html=''.join(web_data[-1:]))
        my_label.grid(column=0, row=1)
        process_container.pack(fill="both", expand=True)
        for child in process_container.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def get_web_data(self, selection) -> str:
        return WebData.get_web_data(WebData, selection[0][1])


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
