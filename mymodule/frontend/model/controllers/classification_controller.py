"""
    Classification controller
"""
import logging
from ....backend.algorithms.classification.classification_algorithms import ClassificationAlgorithms
from generic_algorithm_controller import GenericAlgorithmController

class ClassificationController(GenericAlgorithmController):
    """Controls the position of the axis according to their decomposed values
       It can be configured with dimensionality reduction algorithms such as
       PCA or LDA
    """
    LOGGER = logging.getLogger(__name__)
    PCA_CLASSIFICATION_ID = "PCA"
    LDA_CLASSIFICATION_ID = "LDA"
    DEFAULT_CLASSIFICATION_ID = LDA_CLASSIFICATION_ID

    @staticmethod
    def _get_algorithm_dict():
        """Returns a dictionary with the shape {Algorithm_id, Algorithm}"""
        algorithm_dict = dict()
        algorithm_dict[ClassificationController.PCA_CLASSIFICATION_ID]\
            = ClassificationAlgorithms.pca
        algorithm_dict[ClassificationController.LDA_CLASSIFICATION_ID] \
            = ClassificationAlgorithms.lda
        return algorithm_dict

    def __init__(self, axis_sources, mapper_controller, cluster_controller, algorithm_id=None):
        algorithm_dict = ClassificationController._get_algorithm_dict()
        super(ClassificationController, self).\
              __init__(ClassificationController.DEFAULT_CLASSIFICATION_ID,
                       algorithm_dict,
                       active_algorithm_id=algorithm_id)
        self._axis_sources = axis_sources
        self._mapper_controller = mapper_controller
        self._cluster_controller = cluster_controller

    def relocate_axis(self):
        ClassificationController.LOGGER.debug("Relocating axis classifying with %s",
                                              self.get_active_algorithm_id())
        relocated_axis = None
        dimension_values_df_norm, _ = self._mapper_controller.get_filtered_mapping_df()
        if self.get_active_algorithm_id() == ClassificationController.LDA_CLASSIFICATION_ID:
            relocated_axis = self.execute_active_algorithm(dimension_values_df_norm,
                                                           self._cluster_controller.get_classes())
        else:
            relocated_axis = self.execute_active_algorithm(dimension_values_df_norm)
        for source in self._axis_sources:
            axis_id = source.data['name'][0]
            if self._mapper_controller.is_axis_visible(axis_id):
                source.data['x1'] = [relocated_axis['x'][axis_id]]
                source.data['y1'] = [relocated_axis['y'][axis_id]]
        ClassificationController.LOGGER.debug("Relocation completed")
        return relocated_axis
