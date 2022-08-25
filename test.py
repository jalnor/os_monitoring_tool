import os
from dataclasses import dataclass
import datetime as dt

import mysql
from mysql.connector import cursor
import psutil


@dataclass
class Process:
    name: str
    proc_id: str
    status: str
    started: str


def mydb_connection() -> mysql.connector:
    return mysql.connector.connect(
        host="localhost",
        user=os.environ["db_user"],
        password=os.environ["db_pword"],
        database=os.environ["db"]
    )


def add_process_to_db(func_proc: Process, func_mydb: mysql.connector, func_cursor: mysql.connector.cursor):
    func_cursor.execute(
        "INSERT INTO processes(name, proc_id, status, started) "
        "Values(%s,%s,%s,%s)", (func_proc.name, func_proc.proc_id, func_proc.status, func_proc.started))
    func_mydb.commit()


if __name__ == "__main__":

    procs = {p for p in psutil.process_iter(['name', 'pid', 'status'])}

    mydb = mydb_connection()
    my_cursor = mydb.cursor()

    for p in procs:
        proc = Process(p.name(), p.pid, p.status(), dt.datetime.fromtimestamp(p.create_time()))
        add_process_to_db(proc, mydb, my_cursor)
