import os
from datetime import datetime, timedelta

from sqlmodel import Session, SQLModel, create_engine, select

from db.models import LogHistory, Process, CurrentLog

from functools import wraps
from time import time


def timing(f):
    """A simple timer decorator"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print(f'Elapsed time {f.__name__}: {end - start}')
        return result

    return wrapper


class MyDb:

    def __init__(self):
        self.db_url = os.environ["db_url"]
        self.engine = create_engine(self.db_url, echo=False)
        # self.create_db_and_tables()

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_process_data(self, process_id, hours_ago: int = 24):
        look_back_till = datetime.now() - timedelta(hours=hours_ago)
        breakpoint()
        with Session(self.engine) as session:
            logs = session.exec(
                select(LogHistory).where(
                    LogHistory.process_id == process_id,
                    # LogHistory.captured >= look_back_till
                )
            ).fetchall()
            # print('DB logs...', logs)
            return [(log.proc_id, log.status, log.started, log.captured) for log in logs]
        pass

    @timing
    def get_all_processes(self):
        with Session(self.engine) as session:
            procs = session.exec(select(Process, CurrentLog).join(CurrentLog)
                                 .where(Process.id == CurrentLog.process_id))

            return [(process.id, process.name, currentlog.status,
                     currentlog.proc_id, currentlog.started, currentlog.captured)
                    for process, currentlog in procs]
