""" A simple decorator for computing time cost.

The results will be passed to the logger defined below.
"""
import logging
import time
from common import LOG_FILE
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(LOG_FILE, mode='a')
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

def time_cost(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        time_cost = time.time() - start
        logger.info("The time cost of {} is {}.".format(func.__name__, time_cost))
        return ret
    return wrapper
