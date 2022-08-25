import os
from dataclasses import dataclass
import datetime as dt

import mysql
from mysql.connector import cursor
import psutil

import MyDb


@dataclass
class Process:
    name: str
    proc_id: str
    status: str
    started: str


if __name__ == "__main__":
    procs = {p for p in psutil.process_iter(['name', 'pid', 'status'])}
    my_db = MyDb()
    for p in procs:
        proc = Process(p.name(), p.pid, p.status(), dt.datetime.fromtimestamp(p.create_time()))
        my_db.add_process(proc)
