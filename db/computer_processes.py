import os
from datetime import datetime

import psutil
from sqlmodel import create_engine, SQLModel, Session, select
from dotenv import load_dotenv

from db.models import Process, LogStartStop

load_dotenv()


class ComputerProcesses:

    def __init__(self):
        self.db_url = os.environ["db_url"]
        self.engine = create_engine(self.db_url, echo=True)
        SQLModel.metadata.create_all(self.engine)
        self.create_db_and_tables()
        self.check_processes()

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)
        pass

    def check_processes(self):
        processes = [process for process in psutil.process_iter(['name', 'pid', 'status'])]

        with Session(self.engine) as session:
            results = session.exec(select(Process, LogStartStop).join(LogStartStop)).fetchall()

        if not results:
            self.add_processes_to_db(processes)

        pass

    def add_processes_to_db(self, processes):

        with Session(self.engine) as session:
            try:
                for one_process in processes:

                    process = Process()
                    start_stop = LogStartStop()

                    process.name = one_process.name()
                    process.status = one_process.status()

                    session.add(process)
                    session.commit()

                    start_stop.proc_id = one_process.pid

                    dt = datetime.fromtimestamp(one_process.create_time())
                    if process.status == 'running':
                        start_stop.started = dt
                        start_stop.stopped = None
                    else:
                        start_stop.started = None
                        start_stop.stopped = dt

                    start_stop.process_id = process.id

                    session.add(start_stop)
                    session.commit()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        pass


if __name__ == "__main__":
    ComputerProcesses()
