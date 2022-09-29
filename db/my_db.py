import os
from datetime import datetime as dt, timedelta

from sqlmodel import Session, SQLModel, create_engine, select, and_

from db.models import LogHistory, Process, CurrentLog
from db.pybites_timer import timing


class MyDb:

    def __init__(self):
        self.db_url = os.environ["db_url"]
        self.engine = create_engine(self.db_url, echo=False)
        # self.create_db_and_tables()

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    @timing
    def get_process_data(self, process_id, from_time, till_time):

        with Session(self.engine) as session:
            logs = session.exec(select(LogHistory).where(and_(LogHistory.process_id == process_id,
                                                         LogHistory.captured <= till_time,
                                                         LogHistory.captured >= from_time))).fetchall()
            print('DB logs...', logs)
            # if log.captured >= yesterday
            return [(log.proc_id, log.status, log.started, log.captured) for log in logs]

    @timing
    def get_all_processes(self):
        with Session(self.engine) as session:
            procs = session.exec(select(Process, CurrentLog).join(CurrentLog)
                                 .where(Process.id == CurrentLog.process_id))

            return [(process.id, process.name, currentlog.status,
                     currentlog.proc_id, currentlog.started, currentlog.captured)
                    for process, currentlog in procs]
