from datetime import datetime, date
from typing import Optional, List, Tuple


from sqlmodel import SQLModel, Field


class Process(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    proc_id: str
    status: str


class StartStopTimes(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=Process.id)
    started: datetime
    stopped: datetime


class StartStopDates(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=Process.id)
    capture_date: date
    start_date: date
    stop_date: date

