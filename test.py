from datetime import timedelta, datetime

import mysql
from mysql.connector import cursor

import psutil

import os

import MyDb


class Process():
    name: str
    proc_id: str
    status: str
    started: str

    def __init__(self, name, proc_id, status, start_time):
        self.name = name
        self.proc_id = proc_id
        self.status = status
        self.started = start_time


if __name__ == "__main__":

    procs = {p for p in psutil.process_iter(['name', 'pid', 'status'])}
    print(procs)
    my_cursor: cursor

    mydb = mysql.connector.connect(
        host="localhost",
        user="jnor42",
        password=os.environ["db_pword"],
        database="os_monitoring_tool"
    )

    my_cursor = mydb.cursor()

    for p in procs:
        proc = Process(p.name(), p.pid, p.status(), timedelta(seconds=p.create_time()))
        my_cursor.execute(
            "INSERT INTO processes(name, proc_id, status, started) "
            "Values(%s,%s,%s,%s)", (proc.name, proc.proc_id, proc.status, proc.started))
        mydb.commit()
        # MyDb.add_process(p.name(), p.pid, p.status(), p.create_time())
