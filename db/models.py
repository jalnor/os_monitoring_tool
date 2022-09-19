import time
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
    log_start_stops: List["LogHistory"] = Relationship(back_populates="process")


class CurrentLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proc_id: str
    status: str
    started: datetime
    captured: datetime
    process_id: int = Field(default=None, foreign_key="process.id")
    process: Process = Relationship(back_populates="log_start_stops")


class LogHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proc_id: str
    status: str
    started: datetime
    captured: datetime
    process_id: int = Field(default=None, foreign_key="process.id")
    process: Process = Relationship(back_populates="log_start_stops")

