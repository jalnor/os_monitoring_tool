import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine, select, and_

from db.models import LogHistory, Process, CurrentLog
from db.pybites_timer import timing

load_dotenv()


class MyDb:
    """Defines the database interactions."""
    def __init__(self):
        self.db_url = os.environ["db_url"]
        self.engine = create_engine(self.db_url, echo=False)
        self.create_db_and_tables()

    def create_db_and_tables(self):
        """Create the database tables based on models."""
        SQLModel.metadata.create_all(self.engine)

    # @timing
    def get_process_data(self, process_id, from_time, till_time) -> list[tuple]:
        """Retrieves the process log history and returns as list of tuples."""
        with Session(self.engine) as session:
            logs = session.exec(select(LogHistory).where(and_(LogHistory.process_id == process_id,
                                                         LogHistory.captured <= till_time,
                                                         LogHistory.captured >= from_time))).fetchall()
            return [(log.proc_id, log.status, log.started, log.captured) for log in logs]

    # @timing
    def get_all_processes(self) -> list[tuple]:
        """Retrieves the current process logs and returns as list of tuples."""
        with Session(self.engine) as session:
            procs = session.exec(select(Process, CurrentLog).join(CurrentLog)
                                 .where(Process.id == CurrentLog.process_id))
            return [(process.id, process.name, currentlog.status,
                     currentlog.proc_id, currentlog.started, currentlog.captured)
                    for process, currentlog in procs]
