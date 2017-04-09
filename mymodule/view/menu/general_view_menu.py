"""
    General View Menu
"""

from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import Select, Button, TextInput, Slider

class GeneralViewMenu(object):
    """Basic menu with the principal elements applicable to any view"""
    WIDGETBOX_WIDTH = 50

    @staticmethod
    def _widgetbox(widgets_list, width=WIDGETBOX_WIDTH):
        return widgetbox(widgets_list, responsive=True)

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
        self._view_select = self.init_view_select()
        self._add_view_button = self.init_add_view_button()
        self._new_view_name_input = self.init_view_name_input()

        self._lateral_menu = column(GeneralViewMenu._widgetbox(self._file_select),
                                    GeneralViewMenu._widgetbox(self._mapping_select),
                                    GeneralViewMenu._widgetbox(self._clustering_select),
                                    GeneralViewMenu._widgetbox(self._axis_color_select),
                                    GeneralViewMenu._widgetbox(self._palette_select),
                                    GeneralViewMenu._widgetbox(self._error_select),
                                    GeneralViewMenu._widgetbox([self._initial_size_input,
                                                                self._final_size_input],
                                                               width=80),
                                    GeneralViewMenu._widgetbox(self._new_view_name_input),
                                    GeneralViewMenu._widgetbox(self._add_view_button)
                                   )
        self._view_control_row = row(GeneralViewMenu._widgetbox(self._view_select))

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

    def init_add_view_button(self):
        def new_view():
            self._model.new_add_view_action(self._new_view_name_input.value)
            self._view_select.options = self._model.get_available_views()
            self._view_select.value = self._model.get_active_view_alias()

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
        def select_view(new):
            # Try to select the view only if it is not active already
            if new != self._model.get_active_view_alias():
                self._model.new_view_select_action(new)
        title = "Active view:"
        value = self._model.get_active_view_alias()
        options = self._model.get_available_views()
        callback = select_view 
        return GeneralViewMenu._init_select_widget(title, value, options, callback)

    def init_initial_size_input(self):
        active_initial_size = int(self._model.get_initial_size())
        slider = Slider(start=1, end=40, value=active_initial_size, step=1, title="Initial size")
        slider.on_change('value', lambda attr, old, new:
                         self._model.new_initial_size_action(int(new)))

        return slider

    def init_final_size_input(self):
        active_final_size = int(self._model.get_final_size())
        slider = Slider(start=1, end=40, value=active_final_size, step=1, title="Final size")
        slider.on_change('value', lambda attr, old, new:
                         self._model.new_final_size_action(int(new)))

        return slider

    def init_view_name_input(self):
        value = self._model.get_active_view_alias()
        text_input = TextInput(title="New view:",
                               value=value)
        return text_input

    def get_view_control_layout(self):
        return self._view_control_row

    def get_lateral_menu_layout(self):
        return self._lateral_menu
