import pytest

from db.models import Process, CurrentLog, LogHistory


@pytest.fixture
def process_fixture():
    process = Process()
    process.name = 'fake_process'
    return process


@pytest.fixture
def current_log_fixture():
    current_log = CurrentLog()
    current_log.proc_id = 1340
    current_log.status = 'stopped'
    current_log.started = '2022-09-17 08:02:51.945382'
    current_log.captured = '2022-09-17 19:38:13.754369'
    current_log.process_id = 13
    return current_log


@pytest.fixture
def log_history_fixture():
    log_history = LogHistory()
    log_history.proc_id = 1340
    log_history.status = 'running'
    log_history.started = '2022-09-17 08:02:51.945382'
    log_history.captured = '2022-09-17 19:38:13.754369'
    log_history.process_id = 13
    return log_history


@pytest.mark.parametrize("proc_name", ['fake_process'])
def test_process_create(process_fixture, proc_name):
    assert isinstance(process_fixture, Process)
    assert process_fixture.name == proc_name
    assert process_fixture.__str__() == 'fake_process'


@pytest.mark.parametrize("proc_id, status, started, captured, process_id",
                         [
                             (1340, 'stopped', '2022-09-17 08:02:51.945382',
                              '2022-09-17 19:38:13.754369', 13)
                         ])
def test_create_current_log(current_log_fixture, proc_id, status, started,
                            captured, process_id):
    assert isinstance(current_log_fixture, CurrentLog)
    assert current_log_fixture.proc_id == proc_id
    assert current_log_fixture.status == status
    assert current_log_fixture.started == started
    assert current_log_fixture.captured == captured
    assert current_log_fixture.process_id == process_id
    assert current_log_fixture.__str__() == f'{proc_id} {status} {started} {captured} {process_id}'


@pytest.mark.parametrize("proc_id, status, started, captured, process_id",
                         [
                             (1340, 'running', '2022-09-17 08:02:51.945382',
                              '2022-09-17 19:38:13.754369', 13)
                         ])
def test_create_log_history(log_history_fixture, proc_id, status, started,
                            captured, process_id):
    assert isinstance(log_history_fixture, LogHistory)
    assert log_history_fixture.proc_id == proc_id
    assert log_history_fixture.status == status
    assert log_history_fixture.started == started
    assert log_history_fixture.captured == captured
    assert log_history_fixture.process_id == process_id
    assert log_history_fixture.__str__() == f'{proc_id} {status} {started} {captured} {process_id}'
