from datetime import datetime
from typing import Optional


from sqlmodel import SQLModel, Field


class LogStartStop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proc_id: str
    started: datetime
    stopped: datetime
    process_id: int = Field(default=None, foreign_key="process.id")


class Process(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    status: str

