import tkinter.ttk as ttk

from src.db.graphs import Graph


class CreateWidgets:
    """Create a new ttk notebook tab"""

    def __init__(self, event):
        self.result = event.widget
        self.graph = Graph(figsize=(1, 2), layout='constrained', dpi=100)
        self.selection = [self.result.item(item)['values'] for item in self.result.selection()]
        print()

    # Need a frame def(parent, width, height, padding, borderwidth, relief)
    def create_frame(self, parent, width: int, height: int, padding: int,
                     borderwidth: int, relief: str, style: ttk.Style,
                     grid: list[int], ) -> ttk.Frame:
        frame = ttk.Frame(parent, width=width, height=height,
                          padding=padding, borderwidth=borderwidth,
                          relief=relief, style=style)

        return frame

    # Grid and configure def(column, columnspan, row, rowspan, intial position, weight)
    # def add_grid(self, component, column, columnspan, row, rowspan, sticky, columnconfigure, rowconfigure, weight):
    # Label def(parent, title, justification, grid(column, row,, sticky))

    # Tree def(columns=headers, show=headings, bind=event, grid(column, columnspan, row, rowspan, sticky, in=container it is in)
