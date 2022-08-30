from typing import Optional
import datetime as dt

import psutil
from sqlmodel import SQLModel, Field


def get_processes() -> list[list[str]]:
    # processes_from_db = myDb.get_all_processes()
    proc = Process
    st = StartStopTimes
    sd = StartStopDates
    processes = {p for p in psutil.process_iter(['name', 'pid', 'status'])}
    # print(procs)
    process_str = []
    for process in processes:
        # Check if process still exists
        try:
            proc.name = process.name(),
            proc.proc_id =  process.pid
            proc.status = process.status()

            st.started = dt.datetime.fromtimestamp(process.create_time())
            st.stopped = dt.datetime.fromtimestamp(0)
            sd.capture_date = dt.date.today()
            sd.start_date = dt.date.today()
            sd.stop_date = dt.date(1900, 1, 1)
            process_str.append((proc.name, proc.proc_id, proc.status, st.started, st.stopped,
                                sd.capture_date, sd.start_date, sd.stop_date))
        except psutil.NoSuchProcess:
            pass

    return process_str


class Process(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    proc_id: str
    status: str


class StartStopTimes(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key="process.id")
    started: dt.datetime
    stopped: dt.datetime


class StartStopDates(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key="process.id")
    capture_date: dt.date
    start_date: dt.date
    stop_date: dt.date

