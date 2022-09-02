from sqlmodel import Session, SQLModel, create_engine, select

from db import models


def create_db_and_tables(engine1):
    SQLModel.metadata.create_all(engine1)


def get_data(session, class_name):
    with session:
        statement = select(class_name)
        results = session.exec(statement)
        new_list = []
        for class_name in results:
            new_list.append(class_name)
        return new_list


class MySqliteDb:

    def __init__(self):
        self.sqlite_file_name = "database.db"
        self.sqlite_url = f'sqlite:///{self.sqlite_file_name}'
        self.engine = create_engine(self.sqlite_url, connect_args={'check_same_thread': False}, echo=True)
        create_db_and_tables(self.engine)
        self.session = Session(self.engine)

    def get_all_processes(self):
        new_string = []
        new_process_list = get_data(self.session, models.Process)
        new_times_list = get_data(self.session, models.StartStopTimes)
        new_dates_list = get_data(self.session, models.StartStopDates)
        for i in range(len(new_process_list)):
            new_string.append((new_process_list[i].name, new_process_list[i].proc_id, new_process_list[i].status,
                               new_times_list[i].started, new_times_list[i].stopped,
                               new_dates_list[i].capture_date, new_dates_list[i].start_date, new_dates_list[i].stop_date))
        return new_string
