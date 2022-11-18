from db.graphs import Graph


class create_tab:
    def __init__(self, event):
        self.result = event.widget
        self.graph = Graph(figsize=(1, 2), layout='constrained', dpi=100)
        self.selection = [self.result.item(item)['values'] for item in self.result.selection()]
        print()
