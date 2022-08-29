from unittest.mock import MagicMock, patch

import model.process
import model.process as p


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


# @patch("model.process.psutil.process_iter")
# def test_get_processes(mock_run):
#
#     mock_stdout = MagicMock()
#     mock_stdout.configure_mock(
#         **{
#             "stdout.decode.return_value": processes
#         }
#     )
#     mock_run.return_value = mock_stdout
#
#     result = p.procs
#     assert result == processes
