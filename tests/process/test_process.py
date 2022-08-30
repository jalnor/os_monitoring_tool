from unittest.mock import MagicMock, patch
from db.models import Process as p


# Dummy data
fake_process = p.Process('fake_process', 1234, 'stopped', '17:10:42')
processes = [p.Process('fake_process', 1234, 'stopped', '17:10:42'),
             p.Process('fake_process', 1234, 'stopped', '17:10:42'),
             p.Process('fake_process', 1234, 'stopped', '17:10:42'),
             p.Process('fake_process', 1234, 'stopped', '17:10:42')]


def test_process_create():
    assert fake_process.name == 'fake_process'
    assert fake_process.proc_id == 1234
    assert fake_process.status == 'stopped'
