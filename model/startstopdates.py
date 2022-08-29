from typing import Optional
import datetime as dt

import attr
from sqlmodel import SQLModel, Field


class StartStopDates(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key="process.id")
    capture_date: dt.date
    start_date: dt.date
    stop_date: dt.date

    def __init__(self, cd, start_d, stop_d):
        self.capture_date = cd
        self.start_date = start_d
        self.stop_date = stop_d

    # @property
    # def capture_date(self):
    #     return self.capture_date

    # @attr.setters
    # def capture_date(self, sd: dt.date):
    #     self.capture_date = sd

    # @property
    # def start_date(self):
    #     return self.start_date

    # @attr.setters
    # def start_date(self, sd: dt.date):
    #     self.start_date = sd

    # @property
    # def stop_date(self):
    #     return self.stop_date

    # @attr.setters
    # def stop_date(self, sd: dt.date):
    #     self.stop_date = sd

