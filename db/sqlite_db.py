from sqlmodel import Session, SQLModel, create_engine, select

from db.models import Process


def create_db_and_tables(engine1):
    SQLModel.metadata.create_all(engine1)


class MySqliteDb:

    def __init__(self):

        self.sqlite_file_name = "database.db"
        self.sqlite_url = f'sqlite:///{self.sqlite_file_name}'
        self.engine = create_engine(self.sqlite_url, echo=True)

        create_db_and_tables(self.engine)

        self.session = Session(self.engine)

    def get_all_processes(self):
        self.session.execute("SELECT * FROM process")

    def check_if_proc_exists(self, proc: Process) -> bool:
        print(f'Inside db: {proc}')
        with self.session:
            st = select(Process).where(Process.name == proc.name)
            result = self.session.execute(st)
            print(result)
            if result == '':
                return False
        return True

    def add_processes_to_db(self, proc: Process):
        print(f'Inside db: {proc}')
        self.session.add(proc)

    def get_session(self):
        return self.session

    def commit_session(self):
        self.session.commit()

