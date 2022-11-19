import time
from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


ID = Field(default=None, primary_key=True)
PROCESS_ID = Field(default=None, foreign_key="process.id")
RELATIONSHIP = Relationship(back_populates="log_start_stops")


class Process(SQLModel, table=True):
    """Defines process model.
    Setting up relationships in SQLModel
    https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/
    define-relationships-attributes/
    """
    id: Optional[int] = ID
    name: str = Field(index=True)
    log_start_stops: List["LogHistory"] = Relationship(back_populates="process")


class CurrentLog(SQLModel, table=True):
    """Defines the current log of process model."""
    id: Optional[int] = ID
    proc_id: str
    status: str
    started: datetime
    captured: datetime
    process_id: int = PROCESS_ID
    process: Process = RELATIONSHIP


class LogHistory(SQLModel, table=True):
    """Defines the history of the process."""
    id: Optional[int] = ID
    proc_id: str
    status: str
    started: datetime
    captured: datetime
    process_id: int = PROCESS_ID
    process: Process = RELATIONSHIP
