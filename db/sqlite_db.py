from sqlmodel import Session, SQLModel, create_engine, select

from db.models import Process, LogStartStop


class MySqliteDb:

    def __init__(self):
        self.sqlite_file_name = "C:\\Users\\hal90\\Documents\\PyBites_PDM\\os_monitoring_tool\\database.db"
        self.sqlite_url = f'sqlite:///{self.sqlite_file_name}'
        self.engine = create_engine(self.sqlite_url, echo=True)
        self.create_db_and_tables()

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)
        self.get_all_processes()

    def get_data(self, class_name):
        with Session(self.engine) as session:
            return session.exec(select(class_name)).all()

    def get_all_processes(self):
        new_string = []
        new_process_list = self.get_data(Process)
        new_times_list = self.get_data(LogStartStop)
        if len(new_process_list) != 0:
            for i in range(len(new_process_list)):
                new_string.append((new_process_list[i].name, new_process_list[i].status,
                                   new_times_list[i].proc_id, new_times_list[i].started, new_times_list[i].stopped))
        return new_string
