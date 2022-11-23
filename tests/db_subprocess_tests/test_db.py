import datetime

import pytest
from dotenv import load_dotenv

from db.my_db import MyDb

load_dotenv()


@pytest.fixture
def db_fixture():
    return MyDb(db_url='sqlite:///testing.db')


@pytest.fixture
def time_fixture():
    current_time = datetime.datetime(2022, 11, 18, 21, 2, 27, 710000)
    from_time = datetime.datetime(2022, 11, 18, 21, 2, 27, 700000)
    return from_time, current_time


def test_create_db(db_fixture):
    assert isinstance(db_fixture, MyDb)


@pytest.mark.parametrize("fixture_log_history",
                         [
                             ('18440', 'stopped', datetime.datetime(2022, 11, 18, 20, 59, 00, 806054),
                              datetime.datetime(2022, 11, 18, 21, 2, 27, 706142)),
                         ])
def test_get_process_data(db_fixture, time_fixture, fixture_log_history):
    print('From: ', time_fixture[0], " Till: ", time_fixture[1])
    list_of_log_histories = db_fixture.get_process_data(61, time_fixture[0], time_fixture[1])
    assert list_of_log_histories[0] == fixture_log_history


@pytest.mark.parametrize("expected", [
    (1, 'System Idle Process', 'running', '0', datetime.datetime(1969, 12, 31, 19, 0),
     datetime.datetime(2022, 11, 21, 19, 56, 58, 298577)),
])
def test_get_all_processes(db_fixture, expected):
    list_of_processes = db_fixture.get_all_processes()
    assert list_of_processes[0] == expected

















