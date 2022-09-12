'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
Obtained from StackOverflow @https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
and was originally taken from @https://www.daniweb.com/programming/software-development/threads/350266/creating-table-in-python
'''
import tkinter.font as tkFont
import tkinter.ttk as ttk

from db import my_db


class AllProcesses(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, process_container):
        self.tree = None
        self.procs = []
        self.process_container = process_container
        self._setup_widgets()
        self._build_tree()
        self.db = my_db.MyDb()
        self.refresh_data()

    def _setup_widgets(self):
        information = """click on header to sort by that column
to change width of column drag boundary
        """
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
                        padding=(10, 2, 10, 6), text=information)
        msg.pack(fill='x')
        self.process_container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=process_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
                            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
                            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
                            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.process_container)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.process_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=self.process_container)
        self.process_container.grid_columnconfigure(0, weight=1)
        self.process_container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col in process_header:
            self.tree.heading(col, text=col.title(),
                              command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                             width=tkFont.Font().measure(col.title()))

        for item in self.procs:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                if val is not None:
                    col_w = tkFont.Font().measure(val)
                if self.tree.column(process_header[ix], width=None) < col_w:
                    self.tree.column(process_header[ix], width=col_w)

    def refresh_data(self):
        # Get new processes from db
        self.procs = self.db.get_all_processes()

        # Delete existing values and replace them when tree is rebuilt
        if self.tree.get_children():
            for item in self.tree.get_children():
                self.tree.delete(item)

        self._build_tree()
        # Call the function after one minute to refresh data
        self.process_container.after(60000, self.refresh_data)


def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    # data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
                                                     int(not descending)))


# the test data ...
process_header = ['Name', 'Status', 'Process Id', 'Start Time', 'Capture Time']
