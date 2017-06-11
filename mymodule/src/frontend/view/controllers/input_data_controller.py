"""
    Input Data Controller
"""
import logging
import numbers

class InputDataController(object):
    """Class in charge of holding the raw data coming from the Reader
       and manipulate the data, keeping a centralized copy of it
    """
    LOGGER = logging.getLogger(__name__)

    @staticmethod
    def _split_dimensional_nominal_values(raw_input_df):
        """raw_input_df: (pandas.DataFrame) input as coming from the file
           Returns: (pandas.DataFrame) DataFrame holding the nominal values
                    (pandas.DataFrame) DataFrame holding the numeric values
        """
        #TODO gchicafernandez - Rename repeated labels to guarantee uniqueness
        dimensional_labels = []
        nominal_labels = []
        for i in xrange(len(raw_input_df.columns)):
            if isinstance(raw_input_df.iat[0, i], numbers.Number):
                dimensional_labels.append(raw_input_df.columns[i])
            else:
                nominal_labels.append(raw_input_df.columns[i])

        InputDataController.LOGGER.info("Dimensional columns found: %s", dimensional_labels)
        InputDataController.LOGGER.info("Nominal columns found: %s", nominal_labels)
        dimensional_values_df = raw_input_df.drop(nominal_labels, axis=1, inplace=False)
        nominal_values_df = raw_input_df.drop(dimensional_labels, axis=1, inplace=False)

        return dimensional_values_df, nominal_values_df

    def __init__(self, raw_input_df):
        self._raw_input_df = raw_input_df
        self._dimensional_values_df, self._nominal_values_df\
            = InputDataController._split_dimensional_nominal_values(raw_input_df)
        self._ignored_dimensional_labels = set()
        self._ignored_nominal_labels = set()

    def get_dimensional_values(self, filtered=True):
        if filtered:
            return self.filter_df(self._dimensional_values_df, nominal=False)
        return self._dimensional_values_df

    def get_nominal_values(self, filtered=True):
        if filtered:
            return self.filter_df(self._nominal_values_df, nominal=True)
        return self._nominal_values_df

    def get_number_of_values(self):
        return len(self._raw_input_df.index)

    def get_dimensional_labels(self, filtered=False):
        if not filtered:
            return self._dimensional_values_df.columns.values.tolist()
        all_labels = self.get_dimensional_labels(filtered=False)
        return [label for label in all_labels if not label in self._ignored_dimensional_labels]

    def get_nominal_labels(self, filtered=False):
        if not filtered:
            return self._nominal_values_df.columns.values.tolist()
        all_labels = self.get_nominal_labels(filtered=False)
        return [label for label in all_labels if not label in self._ignored_nominal_labels]

    def get_column_from_raw_input(self, label):
        """Will return a column with all its values extracted from the original DF
           label: (String) unique ID matching a column of the raw input DataFrame
        """
        if not label in self._raw_input_df:
            raise ValueError("""The label '%s', does not match any of the columns
                                from the raw input DataFrame""", label)
        return self._raw_input_df[label]

    def get_element_names(self):
        return self._dimensional_values_df.index

    def get_dimensional_labels_status(self):
        """Returns: list of tuples (label, active)"""
        return [(label, self.is_label_active(label)) \
                for label in self.get_dimensional_labels()]

    def is_label_active(self, label):
        return not label in self._ignored_dimensional_labels\
               and not label in self._ignored_nominal_labels

    def filter_df(self, values_df, axis=1, nominal=False):
        """This method drops from a dataframe the set of ignored values that
           can be either nominal or dimensional depending on the nominal flag.
           It may be used externally in DataFrames derived from dimensional or
           nominal ones, like the vectors DataFrame.
           values_df: (pandas.DataFrame) DataFrame holding the values
           [nominal=False]: (Boolean) whether the ignored labels should be those
           of nominal or dimensional
        """
        filter_set = self._ignored_dimensional_labels
        if nominal:
            filter_set = self._ignored_nominal_labels        
        return values_df.drop(filter_set, axis=axis, inplace=False)

    def update_label_status(self, label_id, active):
        """Adds a dimensional label id to the set of ignored labels if not active,
           otherwise remove it
           label_id: (String) label of the axis as appears in the Dataframe
           active: (Boolean) self explanatory
        """
        if not label_id in self._raw_input_df.columns:
            raise ValueError("label '%s' is not present in the input data labels")

        ignored_set = self._ignored_nominal_labels
        if self.is_dimensional_label(label_id):
            ignored_set = self._ignored_dimensional_labels
        if active:
            InputDataController.LOGGER.debug("Updating label '%s' to active", label_id)
            ignored_set.discard(label_id)
        else:
            InputDataController.LOGGER.debug("Updating label '%s' to NOT active", label_id)
            ignored_set.add(label_id)

    def is_nominal_label(self, label):
        return label in self.get_nominal_labels()

    def is_dimensional_label(self, label):
        return label in self.get_dimensional_labels()

    def is_dimensional_and_active(self, source):
        return self.is_dimensional_label(source) and self.is_label_active(source)
