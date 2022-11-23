import datetime
import os
import time
from pathlib import Path
from unittest.mock import MagicMock

import psutil
import pytest
import sqlmodel
from sqlmodel import Session, select

from db import computer_processes as cp
from db.computer_processes import ComputerProcesses
from db.models import CurrentLog, Process, LogHistory
from db.my_db import MyDb


class FakeProcess:
    def __init__(self, pid, status, create_time):
        self.pid = pid
        self.stat = status
        self.created = create_time

    def create_time(self):
        return self.created

    def status(self):
        return self.stat


@pytest.fixture(scope="session")
def computer_processes_fixture():
    return ComputerProcesses(db_url='sqlite:///testing.db')


@pytest.fixture(scope="session")
def os_processes_fixture():
    return cp.get_os_processes()


@pytest.fixture(scope="session")
def get_cached_processes_fixture(computer_processes_fixture):
    return computer_processes_fixture.get_cached_processes()


@pytest.fixture
def process_fixture():
    fake_process = FakeProcess('1234', 'stopped',
                               datetime.datetime.timestamp(datetime.datetime(2022, 9, 17, 8, 2, 51, 945382)))
    print('Inside process_fixture: ', fake_process.status())
    return fake_process


@pytest.fixture
def get_log_history_fixture():
    db = MyDb(db_url='sqlite:///testing.db')
    return db.get_log_history()


@pytest.fixture
def log_history_fixture():
    log_history = LogHistory()
    log_history.proc_id = 1234
    log_history.status = 'stopped'
    log_history.started = '2022-09-17 08:02:51.945382',
    log_history.captured = '2022-09-17 19:38:13.754369',
    log_history.process_id = 4000
    return log_history


@pytest.fixture
def current_log_fixture():
    current_log = CurrentLog()
    current_log.proc_id = 1234
    current_log.status = 'stopped'
    current_log.started = '2022-09-17 08:02:51.945382',
    current_log.captured = '2022-09-17 19:38:13.754369',
    current_log.process_id = 4000
    return current_log


def test_create_log_history(computer_processes_fixture, process_fixture, log_history_fixture):
    log_history = cp.create_log_history(40, process_fixture)
    assert isinstance(log_history, LogHistory)
    assert log_history.proc_id == process_fixture.pid
    assert log_history.status == process_fixture.status()
    assert log_history.started == datetime.datetime.fromtimestamp(process_fixture.create_time())
    assert isinstance(log_history_fixture, LogHistory)


def test_create_current_log(process_fixture, current_log_fixture):
    current_log = cp.create_current_log(1234, process_fixture)
    assert current_log.proc_id == process_fixture.pid
    assert current_log.status == process_fixture.status()
    assert current_log.started == datetime.datetime.fromtimestamp(process_fixture.create_time())
    assert isinstance(current_log_fixture, CurrentLog)


def test_add_processes_to_db(computer_processes_fixture):
    # Only runs when creating db, coverage will show missing after initial create
    if not Path('testing.db').exists():
        current_processes = cp.get_os_processes()
        computer_processes_fixture.add_processes_to_db(current_processes)
        assert Path('testing.db').exists()
    else:
        assert Path('testing.db').exists()


def test_get_os_processes(os_processes_fixture):
    assert isinstance(os_processes_fixture[0], psutil.Process)
    assert type(os_processes_fixture) == list


def test_get_cached_processes(get_cached_processes_fixture):
    assert type(get_cached_processes_fixture) == set
    assert type(get_cached_processes_fixture.pop()) == tuple


def test_log_entries_by_process_name_id(computer_processes_fixture):
    log_entry = computer_processes_fixture.get_log_entries_by_process_name_id(('svchost.exe', 2772))
    assert isinstance(log_entry, CurrentLog)
    assert log_entry.status == 'running'


def test_create_dif_set(computer_processes_fixture, os_processes_fixture, get_cached_processes_fixture):
    # with Session(computer_processes_fixture.engine) as session:
    os_name_set: set[tuple] = set()
    for process in os_processes_fixture:
        try:
            os_name_set.add((process.name(), process.pid))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.Error):
            # TODO: add logging later
            print("could not retrieve process name, skip")
            # with pytest.raises(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.Error):
            continue
        except Exception as exc:
            print('Could not retrieve name due to some unknown exception: ', exc)
            continue
    dif = get_cached_processes_fixture.difference(os_name_set)
    assert isinstance(dif, set)


@pytest.mark.parametrize("proc_id, status, started, captured, process_id",
                         [
                             ('264', 'running', '2022-11-21 05:57:32.428200', '2022-11-21 19:56:58.475310', 7)
                         ])
def test_get_log_entry_by_pid(computer_processes_fixture, proc_id, status, started, captured, process_id):
    assert isinstance(computer_processes_fixture, ComputerProcesses)
    p = computer_processes_fixture.get_process('svchost.exe')
    assert isinstance(p, Process)
    log_entry = computer_processes_fixture.get_log_entry_by_pid(7, 264)
    assert isinstance(log_entry, CurrentLog)
    assert log_entry.proc_id == proc_id
    assert log_entry.status == status
    assert str(log_entry.started) == started
    assert str(log_entry.captured) == captured
    assert log_entry.process_id == process_id


def test_cp_main(computer_processes_fixture):
    db = MyDb(db_url='sqlite:///testing.db')
    num_records = len(db.get_log_history())
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=30)
    run = computer_processes_fixture
    run()
    while datetime.datetime.now() <= end:
        if (round(time.time()) - round(datetime.datetime.timestamp(start))) % 5 == 0:
            run()
    next_num_records = len(db.get_log_history())
    assert num_records < next_num_records

