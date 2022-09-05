import os
from datetime import datetime

import psutil
from sqlmodel import create_engine, SQLModel, Session, select

from db.models import Process, LogStartStop


class ComputerProcesses:

    def __init__(self):
        self.db_url = os.environ["db_url"]
        self.engine = create_engine(self.db_url, echo=False)
        SQLModel.metadata.create_all(self.engine)
        self.create_db_and_tables()
        self.check_processes()

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)
        pass

    def check_processes(self):
        processes = {process for process in psutil.process_iter(['name', 'pid', 'status'])}

        with Session(self.engine) as session:
            results = session.exec(select(Process, LogStartStop).join(LogStartStop)).fetchall()

        if not results:
            self.add_processes_to_db(processes)
        else:
            for result in results:
                name = result[0].name
                process = [process for process in processes if process.name() == name].pop(0)
                print(process)

        pass

    def add_processes_to_db(self, processes):

        with Session(self.engine) as session:
            for one_process in processes:

                process = Process()
                start_stop = LogStartStop()

                process.name = one_process.name()
                process.status = one_process.status()

                session.add(process)
                session.commit()

                start_stop.proc_id = one_process.pid

                if process.status == 'running':
                    start_stop.started = datetime.fromtimestamp(one_process.create_time())
                    start_stop.stopped = datetime.fromtimestamp(0)
                else:
                    start_stop.started = datetime.fromtimestamp(0)
                    start_stop.stopped = datetime.fromtimestamp(one_process.create_time())

                session.add(start_stop)
                session.commit()

        pass


if __name__ == "__main__":
    ComputerProcesses()
