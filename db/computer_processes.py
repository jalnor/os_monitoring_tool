import os
from datetime import datetime
from typing import Optional, List

import psutil
from sqlmodel import create_engine, SQLModel, Session, select
from dotenv import load_dotenv

from db.models import Process, LogStartStop

load_dotenv()


class ComputerProcesses:

    def __init__(self):
        self.db_url = f'sqlite:///C:\\Users\\hal90\\Documents\\PyBites_PDM\\os_monitoring_tool\\database.db'
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
        print(f'Length of processes list...{len(os_processes)}')
        return os_processes

    def get_cached_processes(self):
        with Session(self.engine) as session:
            cached_processes = session.exec(
                select(Process)
            ).fetchall()
            # sets are faster for lookups than lists
            return {
                proc.name for proc in cached_processes
            }

    def get_process(self, process_name) -> Optional[Process]:
        with Session(self.engine) as session:
            return session.exec(
                select(Process).where(Process.name == process_name)
            ).first()

    def get_log_entries_by_pid(self, pid) -> list[LogStartStop]:
        with Session(self.engine) as session:
            return session.exec(
                select(LogStartStop).where(LogStartStop.proc_id == pid)
            ).fetchall()

    def get_log_entries_by_process_id(self, name):
        with Session(self.engine) as session:
            logs = session.exec(
                select(LogStartStop).join(Process).where(Process.name == name)
            ).fetchall()
            return logs

    def create_log(self, process_id, os_process) -> LogStartStop:
        return LogStartStop(
                            proc_id=os_process.pid,
                            status=os_process.status(),
                            started=datetime.fromtimestamp(os_process.create_time()),
                            captured=datetime.now(),
                            process_id=process_id
                        )

    def update_processes_in_db(self, cached_processes, os_processes):

        with Session(self.engine) as session:
            for os_process in os_processes:
                # more narrow exception: it seems .name() already hits the
                # psutil exception, so in that case skip the rest
                try:
                    name = os_process.name()
                    pid = str(os_process.pid)
                    process = self.get_process(name)
                    # If process doesn't exist in db, add entire process and skip to next iteration
                    if process is None:
                        # new process in db
                        process = Process(
                            name=name
                        )
                        # in spite of the right setup in models.py and
                        # documentation claiming otherwise:
                        # https://sqlmodel.tiangolo.com/tutorial/
                        # relationship-attributes/create-and-update-relationships/
                        # #create-instances-with-relationship-attributes
                        session.add(process)
                        session.commit()
                        # Add log entry at same time as process name for new process
                        log = self.create_log(process.id, os_process)
                        session.add(log)
                        session.commit()
                        continue

                    log_entries = self.get_log_entries_by_pid(pid)

                    # For repeated times adding to db of same named process, need to check if log
                    # entries is empty so, we can add an entry for same name.
                    # This will keep process table small but create entries for different
                    # processes in LogStartStop under same process_id, different pid
                    if not log_entries:
                        log = self.create_log(process.id, os_process)
                        session.add(log)
                        session.commit()
                        continue

                    # For updating existing processes, a.k.a. log_entries has values
                    # Create a new entry if status or started have changed
                    log_entry = log_entries[-1]
                    status = os_process.status()
                    started = datetime.fromtimestamp(os_process.create_time())
                    # check if status or start time have changed, then create new entry
                    if log_entry.status != status or log_entry.started != started:
                        new_log_entry = self.create_log(log_entry.process_id, os_process)
                        session.add(new_log_entry)
                        session.commit()

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # TODO: add logging later
                    print("could not retrieve process name, skip")
                    continue

            # Finally, check if any processes from db are not in os_processes,
            # then check status and update as necessary.
            # Get a set of names from os_processes, then find what db has that os_processes doesn't
            os_name_set = {(process.name()) for process in os_processes}
            dif = cached_processes.difference(os_name_set)
            for proc in dif:

                logs = self.get_log_entries_by_process_id(proc)
                # Hopefully the last entry is the latest one!!!!! :(
                new_log_entry = LogStartStop()
                last_log_entry = logs[-1]

                if last_log_entry.status == 'running':
                    new_log_entry.proc_id = last_log_entry.proc_id
                    new_log_entry.status = 'stopped'
                    new_log_entry.started = last_log_entry.started
                    new_log_entry.captured = datetime.now()
                    new_log_entry.process_id = last_log_entry.process_id

                    session.add(new_log_entry)
                    session.commit()


if __name__ == "__main__":
    cp = ComputerProcesses()
    cp()

