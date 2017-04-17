"""
    Error Register
"""
import logging
from .absolute_sum_error import absolute_sum, ABSOLUTE_SUM_ID
from .square_sum_error import square_sum, SQUARE_SUM_ID
from .max_error import max_error, MAX_ERROR_ID

class ErrorRegister(object):
    """
        Class that registers the available algorithms
    """
    LOGGER = logging.getLogger(__name__)
    # dictionary with the shape {Algorithm_id, Algorithm}
    # holding all registered algorithms
    ALGORITHM_DIC = dict({
        ABSOLUTE_SUM_ID: absolute_sum,
        SQUARE_SUM_ID: square_sum,
        MAX_ERROR_ID: max_error
        })

    @staticmethod
    def get_algorithm_dict():
        """
            Returns the dictionary of available algorithms
        """
        return ErrorRegister.ALGORITHM_DIC
