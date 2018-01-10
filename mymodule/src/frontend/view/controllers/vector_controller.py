"""
    Vector Controller
"""

import logging
from ....backend.util.axis_generator import AxisGenerator
from ....backend.util.df_matrix_utils import DFMatrixUtils

class VectorController(object):
    """Controls the position and available vectors"""

    LOGGER = logging.getLogger(__name__)

    @staticmethod
    def generate_vectors(axis_ids):
        """Will generate the initial set up of vectors using the
           circle subdivision from the AxisGenerator.
           dimensional_values_df: (pandas.DataFrame)
        """
        axis_df = AxisGenerator.generate_star_axis(axis_ids)
        vectors_df = DFMatrixUtils.get_vectors(axis_df)
        return vectors_df

    def __init__(self, input_data_controller):
        self._input_data_controller = input_data_controller
        self._axis_ids = self._input_data_controller.get_dimensional_labels()
        self._vectors_df = VectorController.generate_vectors(self._axis_ids)

    def get_vectors(self, filtered=True):
        """Returns the DataFrame holding the vectors
           [filtered=True]: Filter the vectors by default with the ignored
           dimensional labels from the InputDataController
        """
        if filtered:
            return self._input_data_controller.filter_df(self._vectors_df, axis=0)
        return self._vectors_df

    def update_vector_values(self, new_vectors):
        #TODO gchicafernandez - Use update_single_vector implementation
        VectorController.LOGGER.debug("Updating vector values")
        for vector_id in new_vectors.index:
            self._vectors_df['x'][vector_id] = new_vectors['x'][vector_id]
            self._vectors_df['y'][vector_id] = new_vectors['y'][vector_id]

    def update_single_vector(self, axis_id, x1, y1):
        """Updates the vectors dataframe with the new coordinates
           Typically used when an axis is resized
           axis_id: (String)
           x1: (int)
           y1: (int)
        """
        # We assume that all axis start from the point (0,0)
        # Hence, all vectors are (x1 - 0), (y1 - 0)
        VectorController.LOGGER.debug("Updating vector '%s'", axis_id)
        self._vectors_df.loc[axis_id:axis_id, 'x'] = x1
        self._vectors_df.loc[axis_id:axis_id, 'y'] = y1
