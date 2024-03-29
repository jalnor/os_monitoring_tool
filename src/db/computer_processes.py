import os
import time
from datetime import datetime
from typing import Optional

import psutil
from sqlmodel import create_engine, SQLModel, Session, select
from dotenv import load_dotenv

from src.db.models import Process, LogHistory, CurrentLog
from src.util.file_logger import SaveMessage

load_dotenv()


def create_log_history(process_id, os_process) -> LogHistory:
    return LogHistory(
        proc_id=os_process.pid,
        status=os_process.status(),
        started=datetime.fromtimestamp(os_process.create_time()),
        captured=datetime.now(),
        process_id=process_id
    )


def create_current_log(process_id, os_process) -> CurrentLog:
    return CurrentLog(
        proc_id=os_process.pid,
        status=os_process.status(),
        started=datetime.fromtimestamp(os_process.create_time()),
        captured=datetime.now(),
        process_id=process_id
    )


def get_os_processes():
    os_processes = [
        process for process in psutil.process_iter(['name', 'pid', 'status'])
    ]
    return os_processes


class ComputerProcesses:
    """Captures the running processes and saves or updates them in the database."""

    def __init__(self, db_url=None):
        self.db_url = db_url or os.environ["db_url"]
        self.engine = create_engine(self.db_url, echo=False)
        self.create_db_and_tables()
        self.list_of_current_processes = []
        self.save = SaveMessage()

    def __call__(self):
        os_processes = get_os_processes()
        cached_processes = self.get_cached_processes()
        self.update_processes_in_db(cached_processes, os_processes)

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_cached_processes(self) -> set:
        with Session(self.engine) as session:
            cached_processes = session.exec(
                select(Process, CurrentLog).join(CurrentLog)
            ).fetchall()
            # sets are faster for lookups than lists
            return {
                (proc.name, int(log.proc_id)) for proc, log in cached_processes
            }

    def get_process(self, process_name) -> Optional[Process]:
        with Session(self.engine) as session:
            return session.exec(
                select(Process).where(Process.name == process_name)
            ).first()

    # TODO Check these calls for proper method
    def get_log_entry_by_pid(self, process_id, pid) -> Optional[CurrentLog]:
        with Session(self.engine) as session:
            return session.exec(select(CurrentLog).where(
                CurrentLog.proc_id == pid and CurrentLog.process_id == process_id
            )
            ).first()

    def get_log_entries_by_process_name_id(self, proc) -> Optional[CurrentLog]:
        with Session(self.engine) as session:
            logs = session.exec(
                select(CurrentLog).join(Process).where(Process.name == proc[0], CurrentLog.proc_id == proc[1])
            ).first()
            return logs

    def add_processes_to_db(self, processes, session):
        """Adds the current processes to the database for the first time"""
        for os_process in processes:
            try:
                name = os_process.name()
                process = self.get_process(name)

                if not process:
                    process = Process(
                        name=name
                    )
                    session.add(process)
                    session.commit()

                current_log = create_current_log(process.id, os_process)
                session.add(current_log)

                log_history = create_log_history(process.id, os_process)
                session.add(log_history)

                session.commit()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.Error):
                # TODO: add logging later
                print("could not retrieve process name, skip")
                continue
            except Exception as exc:
                print('Could not retrieve name due to some unknown exception: ', exc)
                continue

    def update_existing_processes(self, dif, session):
        for proc in dif:
            current_log = self.get_log_entries_by_process_name_id(proc)
            if current_log:
                new_log_entry = LogHistory()

                if current_log.status == 'running':
                    new_date = datetime.now()
                    new_log_entry.proc_id = current_log.proc_id
                    new_log_entry.status = 'stopped'
                    new_log_entry.started = current_log.started
                    new_log_entry.captured = new_date
                    new_log_entry.process_id = current_log.process_id
                    session.add(new_log_entry)

                    session.delete(current_log)

                    session.commit()
                else:
                    # print('Deleting log entry: ', current_log)
                    session.delete(current_log)

                    session.commit()

    def create_dif_set(self, os_processes, cached_processes, session):
        os_name_set: set[tuple] = set()
        for process in os_processes:
            try:
                os_name_set.add((process.name(), process.pid))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.Error):
                # TODO: add logging later
                print("could not retrieve process name, skip")
                continue
            except Exception as exc:
                print('Could not retrieve name due to some unknown exception: ', exc)
                continue
        dif = cached_processes.difference(os_name_set)
        self.update_existing_processes(dif, session)

    # @timing
    def update_processes_in_db(self, cached_processes, os_processes):
        with Session(self.engine) as session:
            if cached_processes:

                for os_process in os_processes:
                    # more narrow exception: it seems .name() already hits the
                    # psutil exception, so in that case skip the rest
                    try:
                        name = os_process.name()
                        pid = str(os_process.pid)
                        process = self.get_process(name)
                        # print('Process retrieved from db: ', process)
                        # If process doesn't exist in db, add entire process and skip to next iteration
                        if process is None:
                            # print('No data in db for process: ', os_process)
                            # new process in db
                            process = Process(
                                name=name
                            )
                            session.add(process)
                            session.commit()
                            # Add log entry at same time as process name for new process
                            current_log = create_current_log(process.id, os_process)
                            session.add(current_log)

                            log_history = create_log_history(process.id, os_process)
                            session.add(log_history)

                            session.commit()
                            continue
                        # if processes can change pids, then need to find by more than pid
                        # Use process_id instead
                        current_log = self.get_log_entry_by_pid(process.id, pid)

                        # For repeated times adding to db of same named process, need to check if log
                        # entries is empty so, we can add an entry for same name.
                        # This will keep process table small but create entries for different
                        # processes in LogHistory under same process_id, different pid
                        if not current_log:
                            current_log = create_current_log(process.id, os_process)
                            session.add(current_log)

                            log = create_log_history(process.id, os_process)
                            session.add(log)

                            session.commit()
                            continue

                        # For updating existing processes, a.k.a. log_entries has values
                        status = os_process.status()
                        # check if status or start time have changed, then create new entry
                        if current_log.status != status:
                            current_log.status = status
                            current_log.started = datetime.fromtimestamp(os_process.create_time())
                            session.add(current_log)

                            log_history = create_log_history(process.id, os_process)
                            session.add(log_history)

                            session.commit()
                            continue

                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.Error):
                        # TODO: add logging later
                        print("could not retrieve process name, skip")
                        continue
                    except Exception as exc:
                        print('Could not retrieve name due to some unknown exception: ', exc)
                        continue
            else:
                # Add to db for first time only
                self.add_processes_to_db(os_processes, session)

            # Finally, check if any processes from db are not in os_processes,
            # then check status and update as necessary.
            # Get a set of names from os_processes, then find what db has that os_processes doesn't
            self.create_dif_set(os_processes, cached_processes, session)


if __name__ == "__main__":
    cp = ComputerProcesses()
    cp()
    start_time = round(time.time())
    while True:
        if (round(time.time()) - start_time) % 5 == 0:
            # print('Updating...')
            cp()
