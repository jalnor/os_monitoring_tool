import os

from sqlmodel import Field, Session, SQLModel, create_engine, select

from model import process


def create_db_and_tables(engine1):
    SQLModel.metadata.create_all(engine1)


class MySqliteDb:

    sqlite_file_name = "database.db"
    sqlite_url = f'sqlite:///{sqlite_file_name}'
    engine = create_engine(sqlite_url, echo=True)

    create_db_and_tables(engine)

    session = Session(engine)

    def get_all_processes(self):
        self.session.execute("SELECT * FROM process")

    def check_if_proc_exists(self, proc: process) -> bool:
        print(f'Inside db: {proc}')
        with self.session:
            st = select(process.Process).where(process.Process.name == proc.name)
            result = self.session.execute(st)
            print(result)
            if result == '':
                return False
        return True

    def add_processes_to_db(self, proc: process):
        print(f'Inside db: {proc}')
        self.session.add(proc)

    def get_session(self):
        return self.session

    def commit_session(self):
        self.session.commit()

    @classmethod
    def update_process(cls):
        pass
