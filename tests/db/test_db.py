import os
from datetime import datetime as dt, timedelta
import datetime

import pytest
from dotenv import load_dotenv

from db.my_db import MyDb

load_dotenv()


@pytest.fixture(scope='session')
def db_fixture():
    return MyDb()


@pytest.fixture
def time_fixture():
    current_time = '2022-11-18 21:03:01.369762'
    return dt.now(), dt.now() - timedelta(minutes=3)


def test_create_db(db_fixture):
    assert isinstance(db_fixture, MyDb)


@pytest.mark.parametrize("fixture_log_history",
                         [
                             (18440, 'stopped', '2022-11-18 20:59:00.806054', '2022-11-18 21:02:27.706142', 61),
                             (4416, 'stopped', '2022-11-18 08:17:16.566330', '2022-11-18 21:02:27.695142', 61),
                             (17040, 'stopped', '2022-11-18 20:54:16.705877', '2022-11-18 21:02:27.686142', 13),
                             (4452, 'stopped', '2022-11-18 20:11:38.781955', '2022-11-18 21:02:27.676145', 61),
                             (21292, 'stopped', '2022-11-18 20:59:00.974592', '2022-11-18 21:02:27.664145', 61),
                             (18412, 'stopped', '2022-11-18 20:59:01.897261', '2022-11-18 21:02:27.653939', 61),
                             (3520, 'stopped', '2022-11-18 08:17:16.544455', '2022-11-18 21:02:27.643939', 61),
                             (15760, 'stopped', '2022-11-18 20:54:17.645834', '2022-11-18 21:02:27.632938', 106),
                             (19696, 'stopped', '2022-11-18 08:17:16.248293', '2022-11-18 21:02:27.623941', 175),
                             (15096, 'stopped', '2022-11-18 20:59:00.935892', '2022-11-18 21:02:27.612940', 20),
                             (18732, 'running', '2022-11-18 21:02:11.898392', '2022-11-18 21:02:27.450946', 61),
                             (17792, 'running', '2022-11-18 21:02:21.783776', '2022-11-18 21:02:27.369940', 61),
                             (17400, 'running', '2022-11-18 21:02:11.841394', '2022-11-18 21:02:27.321944', 175),
                             (16672, 'running', '2022-11-18 21:02:21.948339', '2022-11-18 21:02:27.237950', 61),
                             (16416, 'running', '2022-11-18 21:02:21.909479', '2022-11-18 21:02:27.181942', 20),
                             (15588, 'running', '2022-11-18 21:02:11.871745', '2022-11-18 21:02:27.110938', 61),
                             (12272, 'running', '2022-11-18 21:02:22.490731', '2022-11-18 21:02:26.803946', 61),
                             (6692, 'running', '2022-11-18 21:02:12.341443', '2022-11-18 21:02:26.404609', 61),
                         ])
def test_get_process_data(db_fixture, time_fixture, fixture_log_history):
    print('From: ', time_fixture[0], " Till: ", time_fixture[1])
    list_of_log_histories = db_fixture.get_process_data(61, time_fixture[0], time_fixture[1])
    for log_history in list_of_log_histories:
        assert log_history == fixture_log_history


@pytest.mark.parametrize("expected", [
    (1, 'System Idle Process', 'running', '0', datetime.datetime(1969, 12, 31, 19, 0),datetime.datetime(2022, 9, 17, 19, 38, 13, 243291)),
    (2, 'System', 'running', '4', datetime.datetime(1969, 12, 31, 19, 0), datetime.datetime(2022, 9, 17, 19, 38, 13, 295312)),
    (4, '', 'stopped', '72', datetime.datetime(2022, 9, 17, 8, 2, 40, 583152), datetime.datetime(2022, 9, 17, 19, 38, 13, 362292)),
    (5, 'Registry', 'running', '128', datetime.datetime(2022, 9, 17, 8, 2, 40, 723509), datetime.datetime(2022, 9, 17, 19, 38, 13, 387295)),
    (6, 'smss.exe', 'running', '540', datetime.datetime(2022, 11, 13, 7, 45, 52, 301104), datetime.datetime(2022, 11, 13, 8, 51, 15, 769768))
])
def test_get_all_processes(db_fixture, expected):
    list_of_processes = db_fixture.get_all_processes()
    for process in list_of_processes[0:4]:
        assert process == expected
















