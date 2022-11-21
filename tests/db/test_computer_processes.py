import datetime

import psutil
import pytest
import sqlmodel

from db import computer_processes as cp
from db.computer_processes import ComputerProcesses
from db.models import CurrentLog, Process, LogHistory


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
    return ComputerProcesses()


@pytest.fixture
def process_fixture():
    fake_process = FakeProcess('1234', 'stopped',
                               datetime.datetime.timestamp(datetime.datetime(2022, 9, 17, 8, 2, 51, 945382)))
    print('Inside process_fixture: ', fake_process.status())
    return fake_process


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


def test_create_current_log(current_log_fixture):
    assert isinstance(current_log_fixture, CurrentLog)


@pytest.mark.parametrize("proc_id, status, started, captured, process_id",
                         [
                             ('3772', 'running', '2022-11-15 19:30:57.760161', '2022-11-15 21:36:33.591260', 13)
                         ])
def test_get_log_entry_by_pid(computer_processes_fixture, proc_id, status, started, captured, process_id):
    assert isinstance(computer_processes_fixture, ComputerProcesses)
    p = computer_processes_fixture.get_process('svchost.exe')
    assert isinstance(p, Process)
    log_entry = computer_processes_fixture.get_log_entry_by_pid(13, 3772)
    assert isinstance(log_entry, CurrentLog)
    assert log_entry.proc_id == proc_id
    assert log_entry.status == status
    assert str(log_entry.started) == started
    assert str(log_entry.captured) == captured
    assert log_entry.process_id == process_id
