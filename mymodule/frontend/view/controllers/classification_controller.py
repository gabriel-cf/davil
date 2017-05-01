"""
    Classification controller
"""
import logging
from ....backend.algorithms.classification.classification_register import ClassificationRegister
from ....backend.algorithms.classification.lda_classification import LDA_ID
from .abstract_algorithm_controller import AbstractAlgorithmController

class ClassificationController(AbstractAlgorithmController):
    """Controls the position of the axis according to their decomposed values
       It can be configured with dimensionality reduction algorithms such as
       PCA or LDA
    """
    LOGGER = logging.getLogger(__name__)

    CLUSTER_SOURCE_ID = 'Clustering'
    NONE_SOURCE_ID = 'None'

    def __init__(self, input_data_controller, cluster_controller, normalization_controller,
                 axis_sources, algorithm_id=None):
        algorithm_dict = ClassificationRegister.get_algorithm_dict()
        super(ClassificationController, self).\
              __init__(AbstractAlgorithmController.NONE_ALGORITHM_ID,
                       algorithm_dict,
                       active_algorithm_id=algorithm_id,
                       none_algorithm=True)
        self._input_data_controller = input_data_controller
        self._cluster_controller = cluster_controller
        self._normalization_controller = normalization_controller
        self._axis_sources = axis_sources
        self._active_source = ClassificationController.NONE_SOURCE_ID        

    def relocate_axis(self):
        """Executes the classification algorithm and bases on the results
           relocates the axis on the plot. When using LDA, the list of categories
           must have been specified beforehand
        """
        if not self.has_active_algorithm():
            ClassificationController.LOGGER.warn("Could not execute relocation"
                                                 "because there is no active algorithm")
            return
        ClassificationController.LOGGER.debug("Relocating axis classifying with %s",
                                              self.get_active_algorithm_id())
        categories = self.get_categories()
        number_of_categories = len(set(categories))
        relocated_axis = None
        dimension_values_df_norm = self._normalization_controller.get_last_normalized_values()
        if self._is_LDA_active():
            if categories is None\
               or number_of_categories == 0:
                raise ValueError("Attempted to relocate with LDA but no categories\
                                  were specified")
            if number_of_categories < 3:
                raise ValueError("Attempted to relocate with LDA with less than 3 categories")
            relocated_axis = self.execute_active_algorithm(dimension_values_df_norm,
                                                           categories)
        else:
            relocated_axis = self.execute_active_algorithm(dimension_values_df_norm)
        for source in self._axis_sources:
            axis_id = source.data['name'][0]
            if self._input_data_controller.is_label_active(axis_id):
                source.data['x1'] = [relocated_axis['x'][axis_id]]
                source.data['y1'] = [relocated_axis['y'][axis_id]]
        ClassificationController.LOGGER.debug("Relocation completed")
        return relocated_axis

    def update_active_source(self, source_id):
        """Updates the classification source
           source_id: (String) one of the source ids provided by this class
        """
        #if source_id in self.get_available_category_sources():
        self._active_source = source_id

    def get_available_category_sources(self):
        """Returns the list of available sources"""
        # We treat each axis as a source itself with its label as
        def filter_sources(source_l):
            def lda_rule(source):
                if self._is_LDA_active():
                    return self._get_number_of_categories(source) > 2\
                           and not self._input_data_controller.is_dimensional_and_active(source)
                return True
            return [source for source in source_l if lda_rule(source)]
            
        methods_mx = []
        methods_mx.append([ClassificationController.NONE_SOURCE_ID])
        methods_mx.append(filter_sources([ClassificationController.CLUSTER_SOURCE_ID]))
        methods_mx.append(filter_sources(self._input_data_controller.get_nominal_labels()))
        methods_mx.append(filter_sources(self._input_data_controller.get_dimensional_labels()))
        return methods_mx
    
    def get_available_methods(self):
        """Refresh the list of available classification methods based on the
           number of categories. Some methods may need more than two categories
           like LDA
        """
        categories = self.get_categories()
        number_of_categories = len(set(categories))
        available_methods = []
        ClassificationController.LOGGER.debug("Getting available methods with active source"
                                              "'%s' and number of categories '%s'",
                                              self.get_active_source(), number_of_categories)
        available_methods = self.get_all_options()
        if (self._input_data_controller.is_dimensional_and_active(self._active_source)\
           or number_of_categories < 3)\
           and LDA_ID in available_methods:
            available_methods.remove(LDA_ID)

        ClassificationController.LOGGER.debug("Returning available methods '%s'",
                                              available_methods)
        return available_methods

    def get_active_source(self):
        return self._active_source

    def get_categories(self, source=None):
        categories = None
        if source is None:
            if self.in_clustering_mode():
                categories = self._get_categories_from_cluster()
            elif self.in_axis_mode():
                categories = self._get_categories_from_axis()
            else:
                categories = []
            return categories
        else:
            # Swap active source temporarily and call again
            original_source = self._active_source
            self._active_source = source
            categories = self.get_categories(source=None)
            self._active_source = original_source
            return categories

    def in_clustering_mode(self):
        return self._active_source == ClassificationController.CLUSTER_SOURCE_ID

    def in_axis_mode(self):
        return self._active_source in self._input_data_controller.get_nominal_labels()\
               or self._active_source in self._input_data_controller.get_dimensional_labels()

    def in_active_mode(self):
        return self.has_active_algorithm()

    def _is_LDA_active(self):
        return self.get_active_algorithm_id() == LDA_ID

    def _get_categories_from_axis(self, axis_id=None):
        """Updates the categories used for the classification algorithms
           categories: (List<String>) list of class names matching 1:1 with
           the elements of the dimension values DataFrame and in the same order
        """
        axis_id = axis_id
        if axis_id is None:
            axis_id = self._active_source
        ClassificationController.LOGGER.debug("Updating categories from axis '%s'", axis_id)
        categories = self._input_data_controller.get_column_from_raw_input(axis_id).astype(str)
        return categories

    def _get_categories_from_cluster(self):
        ClassificationController.LOGGER.debug("Updating categories from cluster")
        return self._cluster_controller.get_categories()

    def _get_number_of_categories(self, source):
        n_categories = len(set(self.get_categories(source=source)))
        return n_categories


