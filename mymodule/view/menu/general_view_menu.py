"""
    General View Menu
"""

from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import Select, Button, TextInput

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
    def _trigger(widget):
        widget.trigger('value', widget.value, widget.value)

    def __init__(self, model):
        self._model = model
        self._layout = None
        self._init()

    def _init(self):
        self._clustering_select = self.init_clustering_select()
        self._mapping_select = self.init_mapping_select()
        self._error_select = self.init_error_select()
        self._axis_color_select = self.init_axis_color_select()
        self._palette_select = self.init_palette_select()
        self._file_select = self.init_file_select()
        self._initial_size_input = self.init_initial_size_input()
        self._final_size_input = self.init_final_size_input()
        #self._reset_button = self.init_reset_button()
        self._view_select = self.init_view_select()
        self._add_view_button = self.init_add_view_button()

        self._higher_control = row(#widgetbox(self._reset_button), 
                                   widgetbox(self._file_select), 
                                   widgetbox(self._view_select),
                                   widgetbox(self._add_view_button))
        self._lower_control = column([row(widgetbox(self._mapping_select),
                                          widgetbox(self._clustering_select),
                                          widgetbox(self._axis_color_select, self._palette_select)),
                                      row(widgetbox(self._error_select),
                                          widgetbox(self._initial_size_input,
                                                    self._final_size_input))])
        self._layout = column(self._higher_control, self._lower_control)

    def synchronize_view(self):
        """Every widget will execute their callback with their current values
           Except the file widget which will update its value
        """

        GeneralViewMenu._trigger(self._mapping_select)
        GeneralViewMenu._trigger(self._error_select)
        GeneralViewMenu._trigger(self._initial_size_input)
        GeneralViewMenu._trigger(self._final_size_input)
        GeneralViewMenu._trigger(self._palette_select)
        self._view_select.options = self._model.get_available_views()
        self._view_select.value = self._model.get_active_view_alias()
        self.synchronize_colors(new_axis=not self._axis_color_select.value \
                                         in self._model.get_available_axis_ids())

        self._axis_color_select.options = ["None"] + self._model.get_available_axis_ids()

    def synchronize_colors(self, new_axis=False):
        if new_axis:
           self._axis_color_select.value = "None"
           self._axis_color_select.options = ["None"] + self._model.get_available_axis_ids()

    def init_reset_button(self):
        button = Button(label="Reset", button_type="danger", width=50)
        button.on_click(self._model.new_reset_action)
        return button

    def init_add_view_button(self):
        def new_view():
            #alias = self._model.new_add_view_action()
            alias = "SC_{}".format(len(self._view_select.options))
            new_options = []
            for option in self._view_select.options:
                new_options.append(option)
            new_options.append(alias)
            self._view_select.value = alias
            self._view_select.options = new_options
            
        button = Button(label="Add View", button_type="success", width=50)
        button.on_click(new_view)
        return button

    def init_mapping_select(self):
        title = "Mapping Algorithm:"
        value = self._model.get_mapping_algorithm()
        options = self._model.get_mapping_options()
        callback = self._model.new_mapping_select_action
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

    def init_clustering_select(self):
        def new_clustering(new):
            self._model.new_clustering_select_action(new)
            if self._axis_color_select.value != "None":
                self._axis_color_select.value = "None"
        title = "Clustering Algorithm:"
        value = self._model.get_clustering_algorithm()
        options = self._model.get_clustering_options()
        callback = new_clustering
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

    def init_error_select(self):
        title = "Error Algorithm:"
        value = self._model.get_error_algorithm()
        options = self._model.get_error_options()
        callback = self._model.new_error_select_action
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

    def init_axis_color_select(self):
        def select_axis_color(new):
            if new == "None":
                GeneralViewMenu._trigger(self._clustering_select)
            else:
                self._model.new_axis_color_select_action(new)
        title = "Color by axis:"
        value = "None"
        options = ["None"] + self._model.get_available_axis_ids()
        callback = select_axis_color
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

    def init_palette_select(self):
        title = "Palette:"
        options = self._model.get_available_palettes()
        value = options[0]
        callback = self._model.new_palette_select_action
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

    def init_file_select(self):
        title = "Select source file:"
        value = self._model.get_file()
        options = self._model.get_available_files()
        callback = self._model.new_file_select_action
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

    def init_view_select(self):
        title = "Active view:"
        value = self._model.get_active_view_alias()
        options = self._model.get_available_views()
        callback = self._model.new_view_select_action
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

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

    def get_layout(self):
        return self._layout
