import os

from sqlmodel import Session, SQLModel, create_engine, select

from db.models import Process, LogStartStop


class MyDb:

    def __init__(self):
        self.db_url = os.environ["db_url"]
        self.engine = create_engine(self.db_url, echo=True)
        self.create_db_and_tables()

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_all_processes(self):
        new_string = []

        with Session(self.engine) as session:
            list_of_processes = session.exec(select(Process, LogStartStop).join(LogStartStop)).fetchall()
        for process, log in list_of_processes:
            new_string.append((process.name, process.status, log.proc_id, log.started, log.stopped))
        return new_string
