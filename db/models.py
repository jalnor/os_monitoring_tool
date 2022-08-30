from typing import Optional, List
import datetime as dt

import psutil
from sqlmodel import SQLModel, Field

# from model.startstopdates import StartStopDates
# from model.startstoptimes import StartStopTimes


def get_processes() -> list[list[str]]:
    # processes_from_db = myDb.get_all_processes()
    procs = {p for p in psutil.process_iter(['name', 'pid', 'status'])}
    # print(procs)
    process_str = []
    for p in procs:
        # print(p.create_time())
        # Check if process still exists
        try:
            proc = Process(p.name(), p.pid, p.status())
            started = StartStopTimes(dt.datetime.fromtimestamp(p.create_time()), dt.datetime.fromtimestamp(0))
            start_date = StartStopDates(dt.date.today(),
                                        dt.date.today(), dt.date(1900, 1, 1))
            process_str.append((proc.name, proc.proc_id, proc.status, started.started, started.stopped,
                                start_date.capture_date, start_date.start_date, start_date.stop_date))
        except psutil.NoSuchProcess:
            pass

    return process_str


class Process(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    proc_id: str
    status: str

    def __init__(self, name, proc_id, status):
        self.name = name
        self.proc_id = proc_id
        self.status = status


class StartStopTimes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key="process.id")
    started: dt.datetime
    stopped: dt.datetime

    def __init__(self, start, stop):
        self.started = start
        self.stopped = stop


class StartStopDates(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key="process.id")
    capture_date: dt.date
    start_date: dt.date
    stop_date: dt.date

    def __init__(self, cd, start_d, stop_d):
        self.capture_date = cd
        self.start_date = start_d
        self.stop_date = stop_d
