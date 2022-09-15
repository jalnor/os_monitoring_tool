import os

from sqlmodel import Session, SQLModel, create_engine, select

from db.os_processes import OSProcesses
from db.models import LogStartStop


class MyDb:

    def __init__(self):
        self.db_url = os.environ["db_url"]
        self.engine = create_engine(self.db_url, echo=True)
        self.create_db_and_tables()

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_all_processes(self):
        cp = OSProcesses()
        cp()
        return cp.list_of_current_processes

    def get_process_data(self, process_id):
        with Session(self.engine) as session:
            logs = session.exec(select(LogStartStop).where(LogStartStop.process_id == process_id)).fetchall()
            return [(log.proc_id, log.status, log.started, log.captured) for log in logs]
        pass
