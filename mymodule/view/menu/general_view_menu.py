"""
    General View Menu
"""

from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import CheckboxGroup, DataTable, TableColumn, Select, Button, TextInput

class GeneralViewMenu(object):
    """Basic menu with the principal elements applicable to any view"""

    @staticmethod
    def _init_select_widget(title, value, options, on_change_callback):
        """Generic function that creates a Select widget
           title: (String) self descriptive
           value: (String) default selected option
           options: (String[]) self descriptive
           on_change_callback: (Func(String) this is the code to be executed
                                when a new selection is made)
        """
        print options
        select = Select(title=title,
                        value=value,
                        options=options)
        # We pass to the widget an anonymous function with the required parameters
        # for bokeh's on_change method and only the 'new' selected to our function
        select.on_change('value', lambda attr, old, new: on_change_callback(new))
        return select

    @staticmethod
    def _checkbox_update_element(active_list, labels, model_action):
        """Generic function designed to be executed every time a checkbox is checked
           It will call the model informing that the element has been checked
           or unchecked

           active_list: (int[]) list provided by the on_click method of the
                        checkboxgroup
           labels: (String[]) ID labels matching the indexes of the active_list
           model_action: (Func(String, Boolean)) call (to the model) to be executed
        """
        for i in xrange(0, len(labels)):
            element_id = labels[i]
            checked = i in active_list
            model_action(element_id, checked)

    def __init__(self, model):
        self._model = model
        self._layout = None
        self._init()

    def _init(self):
        self._clustering_select = self.init_clustering_select()
        self._mapping_select = self.init_mapping_select()
        self._error_select = self.init_error_select()
        self._file_select = self.init_file_select()
        self._initial_size_input = self.init_initial_size_input()
        self._final_size_input = self.init_final_size_input()
        self._reset_button = self.init_reset_button()
        # The checkboxes are not included with the menu layout
        # They must be placed in the row next to the figure
        self._axis_checkboxes = self.init_axis_checkboxes()

        self._higher_control = row(widgetbox(self._reset_button), widgetbox(self._file_select))
        self._lower_control = column([row(widgetbox(self._mapping_select),
                                          widgetbox(self._clustering_select)),
                                      row(widgetbox(self._error_select),
                                          widgetbox(self._initial_size_input,
                                                    self._final_size_input))])
        self._layout = column(self._higher_control, self._lower_control)

    def init_reset_button(self):
        button = Button(label="Reset", button_type="danger", width=50)
        button.on_click(self._model.new_reset_action)
        return button

    def init_mapping_select(self):        
        title = "Mapping Algorithm:"
        value = self._model.get_mapping_algorithm()
        options = self._model.get_mapping_options()
        callback = self._model.new_mapping_select_action
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

    def init_clustering_select(self):             
        title = "Clustering Algorithm:"
        value = self._model.get_clustering_algorithm()
        options = self._model.get_clustering_options()
        callback = self._model.new_clustering_select_action
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

    def init_error_select(self):
        title = "Error Algorithm:"
        value = self._model.get_error_algorithm()
        options = self._model.get_error_options()
        callback = self._model.new_error_select_action
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

    def init_file_select(self):             
        title = "Select source file:"
        value = self._model.get_file()
        options = self._model.get_available_files()
        callback = self._model.new_file_select_action
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

    def init_axis_checkboxes(self):
        """Generates a group of checkboxes whose function is to activate or
           deactivate the visibility of the axis of the view
        """
        # Get a zipped list of [(element_id, isVisible), ..]
        axis_visibility_list = self._model.get_axis_status()
        print axis_visibility_list
        _ = zip(*axis_visibility_list)
        axis_id_l = [element_id for element_id in _[0]]
        axis_visibility_l = [i for i in xrange(0, len(_[1])) if _[1][i]]
        cb_group = CheckboxGroup(
            labels=axis_id_l,
            active=axis_visibility_l
            )
        cb_group.on_click(lambda active_list: GeneralViewMenu._checkbox_update_element\
                                              (active_list, cb_group.labels, 
                                               self._model.new_axis_checkbox_action))

    def init_initial_size_input(self):
        active_initial_size = str(self._model.get_initial_size())
        text_input = TextInput(title="Initial size:",
                               value=active_initial_size)
        text_input.on_change('value', lambda attr, old, new:
                             self._model.new_initial_size_action(int(new)))

        return text_input

    def init_final_size_input(self):             
        active_final_size = str(self._model.get_final_size())
        text_input = TextInput(title="Final size:",
                               value=active_final_size)
        text_input.on_change('value', lambda attr, old, new:
                             self._model.new_final_size_action(int(new)))

        return text_input

    def get_axis_checkboxes(self):
        return self._axis_checkboxes

    def get_layout(self):
        return self._layout

    #def init_table(self):
    #    """Generates the info table"""
    #    source = self._model.new_table_action()
    #    #source = ColumnDataSource(self._dimension_values_df)
    #    #source.add(self._dimension_values_df.index, name='name')
    #    columns = [TableColumn(field=field, title=field)
    #               for field in self._dimension_values_df.columns.values]
    #    columns.insert(0, TableColumn(field='name', title='name'))
    #    data_table = DataTable(source=source, columns=columns, width=1000, height=600)
    #
    #    return data_table
