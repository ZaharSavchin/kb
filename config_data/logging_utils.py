import logging


def setup_logger(log_file):
    logging.basicConfig(filename=log_file, level=logging.ERROR)
