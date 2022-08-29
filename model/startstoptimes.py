import datetime as dt
from typing import Optional

import attr
from sqlmodel import Field, SQLModel


class StartStopTimes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key="process.id")
    started: dt.time
    stopped: dt.time

    def __init__(self):
        self.started = None
        self.stopped = None

    # @property
    # def started(self):
    #     return self.started
    #
    # @attr.setters
    # def started(self, st: dt.time):
    #     self.started = st
    #
    # @property
    # def started(self):
    #     return self.started
    #
    # @attr.setters
    # def started(self, st: dt.time):
    #     self.started = st
