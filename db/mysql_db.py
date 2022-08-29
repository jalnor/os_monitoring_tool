import os
import mysql.connector


class MyDb:

    def __init__(self):
        self.my_db = mysql.connector.connect(
            host="localhost",
            user=os.environ["db_user"],
            password=os.environ["db_pword"],
            database=os.environ["db"]
        )
        self.my_cursor = self.my_db.cursor()
        self.setup_table()

    def setup_table(self):
        self.my_cursor.execute(
            "CREATE TABLE IF NOT EXISTS processes (name VARCHAR(255), proc_id INT(32), status VARCHAR(255), start_time "
            "TIME)")

    def add_process(self, proc):
        self.my_cursor.execute(
            "INSERT INTO processes(name, proc_id, status, started, stopped, start_date, stop_date) "
            "Values(%s,%s,%s,%s,%s,%s,%s)", (proc.name, proc.proc_id, proc.status, proc.started, proc.stopped,
                                             proc.start_date, proc.stop_date))
        self.my_db.commit()
