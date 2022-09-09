from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class Process(SQLModel, table=True):
    """
    Setting up relationships in SQLModel
    https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/
    define-relationships-attributes/
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    status: str
    log_start_stops: List["LogStartStop"] = Relationship(back_populates="process")


class LogStartStop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proc_id: str
    started: datetime
    process_id: int = Field(default=None, foreign_key="process.id")
    process: Optional[Process] = Relationship(back_populates="log_start_stops")
