import pytest
import sqlmodel

from db.computer_processes import ComputerProcesses
from db.models import CurrentLog, Process


@pytest.fixture(scope="session")
def computer_processes_fixture():
    return ComputerProcesses()


@pytest.mark.parametrize("proc_id, status, started, captured, process_id",
                         [
                             ('3772', 'running', '2022-11-15 19:30:57.760161', '2022-11-15 21:36:33.591260', 13)
                         ])
def test_get_log_entry_by_pid(computer_processes_fixture, proc_id, status, started, captured, process_id):
    assert isinstance(computer_processes_fixture, ComputerProcesses)
    p = computer_processes_fixture.get_process('svchost.exe')
    assert isinstance(p, Process)
    print(p)
    log_entry = computer_processes_fixture.get_log_entry_by_pid(13, 3772)
    print(log_entry)
    assert isinstance(log_entry, CurrentLog)
    assert log_entry.proc_id == proc_id
    assert log_entry.status == status
    assert str(log_entry.started) == started
    assert str(log_entry.captured) == captured
    assert log_entry.process_id == process_id
