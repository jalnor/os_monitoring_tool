import os
from datetime import datetime
from typing import Optional

import psutil
from sqlmodel import create_engine, SQLModel, Session, select
from dotenv import load_dotenv

from db.models import Process, LogStartStop

load_dotenv()


class OSProcesses:

    def __init__(self):
        self.db_url = os.environ["db_url"]
        self.engine = create_engine(self.db_url, echo=False)
        SQLModel.metadata.create_all(self.engine)
        self.create_db_and_tables()

    def __call__(self, *args, **kwargs):
        self.list_of_current_processes = []
        self.update_processes_in_db()

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)
        pass

    def get_processes(self):
        return [process for process in psutil.process_iter(['name', 'pid', 'status'])]

    def get_process(self, process_name, pid) -> Optional[Process]:

        with Session(self.engine) as session:
            return session.exec(
                select(Process).join(LogStartStop).where(Process.name == process_name and LogStartStop.proc_id == pid)
            ).first()

    def get_log_entries_by_pid(self, pid) -> list[LogStartStop]:
        with Session(self.engine) as session:
            return session.exec(
                select(LogStartStop).where(LogStartStop.proc_id == pid)
            ).fetchall()

    def create_log(self, process_id, os_process) -> LogStartStop:
        return LogStartStop(
                            proc_id=os_process.pid,
                            status=os_process.status(),
                            started=datetime.fromtimestamp(os_process.create_time()),
                            captured=datetime.now(),
                            process_id=process_id
                        )

    def add_to_list(self, process, log):
        self.list_of_current_processes.append((log.process_id, process.name, log.status, log.proc_id,
                                               str(log.started).split('.')[0], str(log.captured).split('.')[0]))

    def update_processes_in_db(self):
        os_processes = self.get_processes()
        with Session(self.engine) as session:
            for os_process in os_processes:
                # psutil exception, so in that case skip the rest
                try:
                    name = os_process.name()
                    pid = str(os_process.pid)
                    process = self.get_process(name, pid)
                    # print('Got process: ', process)
                    # If process doesn't exist in db, add entire process and skip to next iteration
                    if process is None:
                        # print('Inside new process', process)
                        # new process in db
                        process = Process(
                            name=name
                        )
                        # # Add log entry at same time as process name for new process
                        log = self.create_log(process.id, os_process)
                        if (process.name, log.status, log.proc_id, log.started,
                                log.captured) not in self.list_of_current_processes:
                            self.add_to_list(process, log)
                        continue

                    log_entries = self.get_log_entries_by_pid(pid)
                    # print('Got log entries: ', log_entries)
                    # For repeated times adding to db of same named process, need to check if log
                    # entries is empty so, we can add an entry for same name.
                    # This will keep process table small but create entries for different
                    # processes in LogStartStop under same process_id, different pid
                    if not log_entries:
                        # print('Inside no entries', process)
                        log = self.create_log(process.id, os_process)
                        if (process.name, log.status, log.proc_id, log.started,
                                log.captured) not in self.list_of_current_processes:
                            self.add_to_list(process, log)
                        continue

                    # For updating existing processes, a.k.a. log_entries has values
                    # Create a new entry if status or started have changed
                    log_entry = log_entries[-1]
                    status = os_process.status()
                    started = datetime.fromtimestamp(os_process.create_time())
                    # check if status or start time have changed, then create new entry
                    if log_entry.status != status or log_entry.started != started:
                        new_log_entry = self.create_log(log_entry.process_id, os_process)
                        if (process.name, new_log_entry.status, new_log_entry.proc_id, new_log_entry.started,
                                new_log_entry.captured) not in self.list_of_current_processes:
                            # print('Adding to list', process)
                            self.add_to_list(process, new_log_entry)
                    else:
                        # print('End of line with process: ', process)
                        # print('And log: ', log_entry)
                        self.add_to_list(process, log_entry)

                    # print(len(self.list_of_current_processes))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # TODO: add logging later
                    print("could not retrieve process name, skip")
                    continue


