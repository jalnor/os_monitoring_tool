import logging
import sys

# TODO Refactor this into log to file to enable adjusting format for different scenarios
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


class SaveMessage:
    def __init__(self, fmt=None, *args, **kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.fmt.format(*self.args, **self.kwargs)


def log_to_file(name, log_file=None, level=logging.DEBUG, file_handler=False):
    if file_handler:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
