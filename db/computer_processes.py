import os
from datetime import datetime
from typing import Optional

import psutil
from sqlmodel import create_engine, SQLModel, Session, select
from dotenv import load_dotenv

from db.models import Process, LogStartStop

load_dotenv()


class ComputerProcesses:

    def __init__(self):
        self.db_url = os.environ["db_url"]
        self.engine = create_engine(self.db_url, echo=False)

    def __call__(self):
        self.create_db_and_tables()
        os_processes = self.get_os_processes()
        cached_processes = self.get_cached_processes()
        self.update_processes_in_db(cached_processes, os_processes)

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_os_processes(self):
        os_processes = [
            process for process in psutil.process_iter(['name', 'pid', 'status'])
        ]
        return os_processes

    def get_cached_processes(self):
        with Session(self.engine) as session:
            cached_processes = session.exec(
                select(LogStartStop)
            ).fetchall()
            # sets are faster for lookups than lists
            return {
                (proc.process_id, proc.proc_id) for proc in cached_processes
            }

    def get_process(self, process_name) -> Optional[Process]:
        with Session(self.engine) as session:
            return session.exec(
                select(Process).where(Process.name == process_name)
            ).first()

    def get_log_entries_by_pid(self, pid) -> Optional[Process]:
        with Session(self.engine) as session:
            return session.exec(
                select(LogStartStop).where(LogStartStop.proc_id == pid)
            ).fetchall()

    def update_processes_in_db(self, cached_processes, os_processes):
        with Session(self.engine) as session:
            for os_process in os_processes:
                # more narrow exception: it seems .name() already hits the
                # psutil exception, so in that case skip the rest
                try:
                    name = os_process.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # TODO: add logging later
                    print("could not retrieve process name, skip")
                    continue

                pid = str(os_process.pid)
                process = self.get_process(name)

                if process is None:
                    # new process in db
                    process = Process(
                        name=name,
                        status=os_process.status()
                    )
                    # I don't like the extra commits but without them I could
                    # not get it to work :(
                    # in spite of the right setup in models.py and
                    # documentation claiming otherwise:
                    # https://sqlmodel.tiangolo.com/tutorial/
                    # relationship-attributes/create-and-update-relationships/
                    # #create-instances-with-relationship-attributes
                    session.add(process)
                    session.commit()

                log_entries = self.get_log_entries_by_pid(pid)
                if len(log_entries) == 0:
                    # new log entry
                    entry = LogStartStop(
                        proc_id=pid,
                        started=datetime.now(),
                        # process=process <-- could not get this to work
                        process_id=process.id
                    )
                    session.add(entry)
                    log_entries = [entry]
                    session.commit()

                # existing process, mark related entries as complete (add end date)
                for entry in log_entries:
                    if entry.stopped is not None:
                        # nothing to do, we don't want to override existing end date
                        continue

                    if cached_processes and (process.id, pid) not in cached_processes:
                        # process not active anymore, mark ended
                        entry.stopped = datetime.now()
                        print("setting end time for process", process)
                        session.add(entry)

            # this commit should be able to batch all added entries
            session.commit()


if __name__ == "__main__":
    cp = ComputerProcesses()
    cp()
