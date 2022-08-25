import mysql.connector
from mysql.connector import cursor
import os
import test


class MyDb:

    def __init__(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user=os.environ["db_user"],
            password=os.environ["db_pword"],
            database=os.environ["db"]
        )
        my_cursor = self.mydb.cursor()
        print('In there')
        self.setup_table()

    def setup_table(self):
        self.my_cursor.execute(
            "CREATE TABLE IF NOT EXISTS processes (name VARCHAR(255), proc_id INT(32), status VARCHAR(255), start_time "
            "TIME)")

    def add_process(self, proc):
        self.my_cursor.execute(
                "INSERT INTO processes(name, proc_id, status, started) "
                "Values(%s,%s,%s,%s)", (proc.name, proc.proc_id, proc.status, proc.started))
        self.mydb.commit()
