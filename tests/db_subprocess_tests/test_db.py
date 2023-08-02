import datetime
from unittest.mock import MagicMock

import pytest
from dotenv import load_dotenv

from src.db.my_db import MyDb

load_dotenv()


@pytest.fixture
def db_fixture():
    return MyDb(db_url='sqlite:///testing.db')


@pytest.fixture
def time_fixture():
    current_time = datetime.datetime(2022, 11, 21, 20, 0, 0, 0)
    from_time = datetime.datetime(2022, 11, 21, 19, 0, 0, 0)
    return from_time, current_time


def test_create_db(db_fixture):
    assert isinstance(db_fixture, MyDb)


# Only works on Windows, not os independent!
@pytest.mark.parametrize("expected",
                         [
                             ('3924', 'stopped', datetime.datetime(2022, 11, 20, 15, 7, 28, 123794),
                              datetime.datetime(2022, 11, 21, 19, 57, 2, 766221)),
                         ]) # 200,13924,running,2022-11-20 15:07:28.123794,2022-11-21 19:57:02.766221,7
def test_get_process_data(db_fixture, time_fixture, expected):
    mock_cursor = MagicMock()
    mock_cursor.configure_mock(
        **{"get_process_data.return_value": expected}
    )
    setattr(db_fixture, "sqlmodel_orm", mock_cursor)
    list_of_log_histories = db_fixture.get_process_data(mock_cursor)
    assert expected in list_of_log_histories


# Only works on Windows, not os independent!
@pytest.mark.parametrize("expected", [
    (1, 'System Idle Process', 'running', '0', datetime.datetime(1969, 12, 31, 19, 0),
     datetime.datetime(2022, 11, 21, 19, 56, 58, 298577)),
])
def test_get_all_processes(db_fixture, expected):
    list_of_processes = db_fixture.get_all_processes()
    assert list_of_processes[0] == expected
