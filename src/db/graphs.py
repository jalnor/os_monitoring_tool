import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

matplotlib.use('TkAgg')


class Graph:
    def __init__(self, figsize: tuple, layout: str, dpi: int):
        self.fig, self.ax = plt.subplots(figsize=figsize, layout=layout,
                                         dpi=dpi)
        self.data_for_process = []
        self.list_of_statuses = []
        self.ax2 = self.ax.twiny()

    def set_major_stuff(self):
        plt.xlim(xmin=0.0)

        plt.ylim(ymin=0.0)

        time_lists = []
        x_minor = [dt[2].time().strftime('%H:%M:%S') for dt in self.data_for_process]

        x_minor_floats = [float(x) for x in range(0, len(x_minor))]

        x_major = list(dict.fromkeys([str(dt[2]).split(' ')[0] for dt in self.data_for_process]))

        for x in x_major:
            time_lists.append(
                [y[2].time().strftime('%H:%M:%S') for y in self.data_for_process if str(y[2]).split(" ")[0] == x])

        x_major_locations = [0.0]
        last_x = 0
        for x in time_lists[:(len(time_lists) - 1)]:
            x_major_locations.append(len(x) + last_x + 1)
            last_x += len(x)

        self.ax.plot(self.list_of_statuses, label='Status')

        self.ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        self.ax2.format_xdata = mdates.DateFormatter('%H:%M:%S')

        self.ax.set_yticks(ticks=[0.0, 1.0], labels=['Stopped', 'Running'], rotation=45)

        self.ax.minorticks_off()
        self.ax.tick_params(which='major', length=8, width=2, color='blue', labelcolor='blue', bottom=True,
                            top=False, labeltop=False, labelbottom=True, pad=40, rotation=20)
        self.ax.set_xticks(ticks=x_major_locations, labels=x_major, minor=False)

        self.ax2.minorticks_on()
        self.ax2.xaxis.set_minor_locator(MultipleLocator(1))
        self.ax2.yaxis.set_minor_locator(MultipleLocator(1))
        self.ax2.tick_params(axis='x', which='minor', length=4, color='red', labelcolor='red', rotation=70, bottom=True,
                             top=False, labeltop=False, labelbottom=True, labelsize=8, direction='in')
        self.ax2.set_xticks(ticks=x_minor_floats, labels=x_minor, minor=True)

        self.ax.set_title('Status')
        self.ax.legend()

    def set_frame(self, frame):
        return FigureCanvasTkAgg(self.fig, master=frame)

    # TODO finish refactoring this class
    def set_tick_marks(self):
        print()

    def close_plot(self):
        plt.close(self.fig)
