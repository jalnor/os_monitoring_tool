import datetime
import time
from typing import Optional
import datetime as dt
import os

import psutil
from sqlmodel import Field, Session, SQLModel, create_engine

from model.startstopdates import StartStopDates
from model.startstoptimes import StartStopTimes

try:
    import tkinter as tk
    import tkFont
    import ttk
except ImportError:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk

from psutil import Process
from db.sqlite_db import MySqliteDb
from ui.main_ui import MainUi
from model import process


def create_db_and_tables(engine1):
    SQLModel.metadata.create_all(engine1)


def start_ui():
    return MainUi()


if __name__ == "__main__":
    my_ui = start_ui()

    ''' This is the sqlite setup for handling database '''
    # sqlite_file_name = "database.db"
    # sqlite_url = f'sqlite:///{sqlite_file_name}'
    # engine = create_engine(sqlite_url, echo=True)
    #
    # if not os.path.isfile(sqlite_url):
    #     create_db_and_tables(engine)
    #
    # procs = process.get_processes()
    # # my_db = MyDb()
    # count = 1
    # session = Session(engine)
    # print(procs)
    # for p in procs:
    #     proc = (p[0], p[1], p[2])
    #     # times = (StartStopTimes.started(p[3]), StartStopTimes.stopped(p[4]))
    #     # dates = (StartStopDates.start_date(p[5]), StartStopDates.stop_date(p[6]))
    #     # started = StartStopTimes.started(dt.datetime.fromtimestamp(p.create_time()))
    #     # current_date = StartStopDates.start_date(dt.now())
    #     session.add(proc)
    #     # session.add(times)
    #     # session.add(dates)
    #     # my_db.add_process(proc)
    # session.commit()
    # session.close()
