from datetime import datetime, timedelta
import os

import psutil
from sqlmodel import Session, SQLModel, create_engine, select

from db.models import Process, LogStartStop


class MyDb:

    def __init__(self):
        self.db_url = os.environ["db_url"]
        self.engine = create_engine(self.db_url, echo=True)
        self.create_db_and_tables()
        # Checking if app pid in result set
        print("The app pid is: ", os.getpid())

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_os_processes(self):
        return {
            (process.name(), process.pid) for process in psutil.process_iter(['name', 'pid', 'status'])
        }

    def get_all_processes(self):
        new_string = []

        with Session(self.engine) as session:
            list_of_processes = session.exec(select(Process, LogStartStop).join(LogStartStop)).fetchall()

        os_processes = self.get_os_processes()

        for process, log in list_of_processes:
            if (process.name, int(log.proc_id)) in os_processes:
                new_string.append((process.name, log.status, log.proc_id, log.started, log.captured))
        return new_string
