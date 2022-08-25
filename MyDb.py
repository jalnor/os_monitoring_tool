import mysql.connector
from mysql.connector import cursor
import os
import test


def setup_table(self):
    self.my_cursor.execute(
        "CREATE TABLE IF NOT EXISTS processes (name VARCHAR(255), proc_id INT(32), status VARCHAR(255), start_time "
        "TIME)")


def add_process(self, name, proc_id, status, started):
    self.my_cursor.execute(
            "INSERT INTO processes(name, proc_id, status, started) "
            "Values(%s,%s,%s,%s)", (name, proc_id, status, started))
    self.mydb.commit()


class MyDb:
    my_cursor: cursor
    mydb: mysql.connector

    def __init__(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="jnor42",
            password=os.environ["db_pword"],
            database="os_monitoring_tool"
        )

        print('In there')

        my_cursor = mydb.cursor()
        setup_table(my_cursor)

