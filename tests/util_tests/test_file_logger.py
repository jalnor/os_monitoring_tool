import inspect
import logging

from util import file_logger as fl
from util.file_logger import SaveMessage


HELLO = 'Hello World!'


def test_file_logger():
    frame = inspect.currentframe()
    name = inspect.getframeinfo(frame)
    file_logger = fl.log_to_file(name=name.function, log_file='testing.log',
                                 level=logging.DEBUG, file_handler=True)
    message = SaveMessage
    file_logger.debug(msg=message(f'{name.function}: Expected output! {HELLO}').__str__())
    print(inspect.getframeinfo(frame).function)
    # assert isinstance(file_logger.name, )


def test_console_logger():
    frame = inspect.currentframe()
    name = inspect.getframeinfo(frame)
    console_logger = fl.log_to_file(name=name.function)
    message = SaveMessage
    console_logger.debug(msg=message(f'{name.function}: This should print to console! {HELLO}').__str__())
