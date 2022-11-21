import inspect
import logging

from util import file_logger as fl
from util.file_logger import SaveMessage


HELLO = 'Hello World!'


def test_file_logger():
    frame = inspect.currentframe()
    file_logger = fl.log_to_file(name=inspect.getframeinfo(frame).function, log_file='testing.log',
                                 level=logging.DEBUG, file_handler=True)
    message = SaveMessage
    file_logger.debug(msg=message(f'Expected output! {0}', HELLO).__str__())
    print(inspect.getframeinfo(frame).function)
    # assert isinstance(file_logger.name, )


def test_console_logger():
    frame = inspect.currentframe()
    console_logger = fl.log_to_file(name=inspect.getframeinfo(frame).function)
    message = SaveMessage
    console_logger.debug(msg=message(f'This should print to console! {0}', HELLO).__str__())
