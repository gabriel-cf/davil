"""
    Mapping Register
"""
import logging
from .star_coordinates_mapper import star_coordinates, STAR_COORDINATES_ID
from .dummy_coordinates_mapper import dummy_coordinates, DUMMY_COORDINATES_ID

class MappingRegister(object):
    """
        Class that registers the available algorithms
    """
    LOGGER = logging.getLogger(__name__)
    # dictionary with the shape {Algorithm_id, Algorithm}
    # holding all registered algorithms
    ALGORITHM_DIC = dict({
        STAR_COORDINATES_ID: star_coordinates
        #DUMMY_COORDINATES_ID: dummy_coordinates # For demonstration and testing purposes
        })

    @staticmethod
    def get_algorithm_dict():
        """
            Returns the dictionary of available algorithms
        """
        return MappingRegister.ALGORITHM_DIC
