"""
    General View Menu
"""

import logging
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import Select, Button, TextInput, Slider, Dropdown, RadioButtonGroup, Div
from .widgets.select_widget import SelectWidget
from .widgets.slider_widget import SliderWidget
from .widgets.radio_widget import RadioWidget
from .widgets.dropdown_widget import DropdownWidget

class GeneralViewMenu(object):
    """Basic menu with the principal elements applicable to any view"""
    LOGGER = logging.getLogger(__name__)
    WIDGETBOX_WIDTH = 50
    NONE = "None"

    @staticmethod
    def _get_title_div(text):
        div = Div(text="""{}""".format(text), height=1)
        return div

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
        select = Select(title=title,
                        value=value,
                        options=GeneralViewMenu._sort_options(options))
        # We pass to the widget an anonymous function with the required parameters
        # for bokeh's on_change method and only the 'new' selected to our function
        select.on_change('value', lambda attr, old, new: on_change_callback(new))
        return select

    @staticmethod
    def _trigger(widget):
        if isinstance(widget, RadioButtonGroup):
            widget.trigger('active', widget.active, widget.active)
        else:
            widget.trigger('value', widget.value, widget.value)

    @staticmethod
    def _sort_options(options):
        """Custom sort of options coming from backend
           Will position first 'None' if found
        """
        res_options = []
        if GeneralViewMenu.NONE in options:
            res_options.append(GeneralViewMenu.NONE)
            options.remove(GeneralViewMenu.NONE)
        options.sort()
        return res_options + options

    def __init__(self, model):
        self._model = model
        self._layout = None
        self._init()

    def _init(self):
        self._clustering_select = self.init_clustering_select()
        self._mapping_select = self.init_mapping_select()
        self._normalization_select = self.init_normalization_select()
        self._error_select = self.init_error_select()
        self._axis_select = self.init_axis_select()
        self._palette_select = self.init_palette_select()
        self._file_select = self.init_file_select()
        self._number_of_clusters_input = self.init_number_of_clusters_input()
        self._initial_size_input = self.init_initial_size_input()
        self._final_size_input = self.init_final_size_input()
        self._classification_select = self.init_classification_select()
        self._view_select = self.init_view_select()
        self._add_view_button = self.init_add_view_button()
        self._new_view_name_input = self.init_view_name_input()
        self._category_source_dropdown = self.init_category_source_dropdown()
        self._color_method_radio = self.init_color_method_radio()
        self._point_label_radio = self.init_point_label_radio()

        self._lateral_menu = column(GeneralViewMenu._widgetbox(self._file_select.widget),
                                    GeneralViewMenu._widgetbox(self._mapping_select.widget),
                                    GeneralViewMenu._widgetbox(self._normalization_select.widget),
                                    GeneralViewMenu._widgetbox(self._clustering_select.widget),
                                    GeneralViewMenu._widgetbox(self._number_of_clusters_input.widget),
                                    GeneralViewMenu._widgetbox(self._error_select.widget),
                                    GeneralViewMenu._widgetbox([self._initial_size_input.widget,
                                                                self._final_size_input.widget]),
                                    GeneralViewMenu._get_title_div("Toggle point names:"),
                                    GeneralViewMenu._widgetbox(self._point_label_radio.widget)
                                   , name='lateral_menu')
        self._upper_menu = row(GeneralViewMenu._widgetbox(self._classification_select.widget),
                               GeneralViewMenu._widgetbox(self._view_select.widget)
                               , name='upper_menu')
        self._upper_right_menu = column(GeneralViewMenu._widgetbox(self._new_view_name_input),
                                        GeneralViewMenu._widgetbox(self._add_view_button)
                                  , name='upper_right_menu')
        self._right_menu = column(GeneralViewMenu._get_title_div("Color by:"),
                                  GeneralViewMenu._widgetbox(self._color_method_radio.widget),
                                  GeneralViewMenu._get_title_div("Selected category source:"),
                                  GeneralViewMenu._widgetbox(self._category_source_dropdown.widget),
                                  GeneralViewMenu._widgetbox(self._axis_select.widget),
                                  GeneralViewMenu._widgetbox(self._palette_select.widget))

    def synchronize_view(self):
        """Every widget will execute their callback with their current values
           Except the file widget which will update its value
           Should happen when a new view is created
        """
        self._mapping_select.trigger()
        self._normalization_select.trigger()
        self._error_select.trigger()
        self._clustering_select.trigger()
        self._number_of_clusters_input.trigger()
        self._initial_size_input.trigger()
        self._final_size_input.trigger()
        self._point_label_radio.trigger()
        self._palette_select.trigger()

        self._axis_select.trigger()
        self._category_source_dropdown.trigger()
        self._color_method_radio.trigger()
        #self._classification_select.trigger()
        self._axis_select.trigger()

        self._view_select.update_options()
        self._view_select.update_value()

    def synchronize_menu(self):
        self._mapping_select.update_all()
        self._normalization_select.update_all()
        self._error_select.update_all()
        self._clustering_select.update_all()
        self._number_of_clusters_input.update_all()
        self._initial_size_input.update_all()
        self._final_size_input.update_all()
        self._point_label_radio.update_all()
        self._palette_select.update_all()

        self._axis_select.update_all()
        self._category_source_dropdown.update_all()
        self._color_method_radio.update_all()
        #self._classification_select.update_all()
        self._axis_select.update_all()

        self._view_select.update_options()
        self._view_select.update_value()

    def synchronize_menu(self):
        """Synchronizes options and values based on the current view
           Should happen when switching back to an existing view
        """
        pass

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
        update_value_callback = self._model.get_mapping_algorithm
        update_options_callback = self._model.get_mapping_options
        on_change_callback = self._model.new_mapping_select_action
        return SelectWidget.init_select_widget(title, update_value_callback, 
                                               update_options_callback, on_change_callback)

    def init_normalization_select(self):
        title = "Normalization Algorithm:"
        update_value_callback = self._model.get_normalization_algorithm
        update_options_callback = self._model.get_normalization_options
        on_change_callback = self._model.new_normalization_select_action
        return SelectWidget.init_select_widget(title, update_value_callback, 
                                               update_options_callback, on_change_callback)

    def init_clustering_select(self):
        title = "Clustering Algorithm:"
        update_value_callback = self._model.get_clustering_algorithm
        update_options_callback = self._model.get_clustering_options
        on_change_callback = self._model.new_clustering_select_action

        return SelectWidget.init_select_widget(title, update_value_callback, 
                                               update_options_callback, on_change_callback)

    def init_error_select(self):
        title = "Error Algorithm:"
        update_value_callback = self._model.get_error_algorithm
        update_options_callback = self._model.get_error_options
        on_change_callback = self._model.new_error_select_action
        return SelectWidget.init_select_widget(title, update_value_callback, 
                                               update_options_callback, on_change_callback)

    def init_axis_select(self):
        title = "Selected axis:"
        update_value_callback = self._model.get_selected_axis_id
        update_options_callback = self._model.get_available_axis_ids
        on_change_callback = self._model.new_axis_select_action
        return SelectWidget.init_select_widget(title, update_value_callback, 
                                               update_options_callback, on_change_callback)

    def init_palette_select(self):
        title = "Palette:"
        update_value_callback = self._model.get_palette
        update_options_callback = self._model.get_available_palettes      
        on_change_callback = self._model.new_palette_select_action
        return SelectWidget.init_select_widget(title, update_value_callback, 
                                               update_options_callback, on_change_callback)

    def init_file_select(self):
        title = "Select source file:"
        update_value_callback = self._model.get_file
        update_options_callback = self._model.get_available_files
        on_change_callback = self._model.new_file_select_action
        return SelectWidget.init_select_widget(title, update_value_callback, 
                                               update_options_callback, on_change_callback)

    def init_classification_select(self):
        def new_classification(new):            
            self._model.new_classification_action(new)
            self._synchronize_sources()
        title = "Axis classification method:"
        update_value_callback = self._model.get_classification_algorithm
        update_options_callback = self._model.get_classification_methods
        on_change_callback = new_classification
        return SelectWidget.init_select_widget(title, update_value_callback, 
                                               update_options_callback, on_change_callback)

    def init_view_select(self):
        def select_view(new):
            # Try to select the view only if it is not active already
            if new != self._model.get_active_view_alias():
                self._model.new_view_select_action(new)
        title = "Active view:"
        update_value_callback = self._model.get_active_view_alias
        update_options_callback = self._model.get_available_views
        on_change_callback = select_view 
        return SelectWidget.init_select_widget(title, update_value_callback, 
                                               update_options_callback, on_change_callback)

    def init_category_source_dropdown(self):
        def new_category_source(new):
            self._model.new_category_source_select_action(new)
            self._synchronize_classification()            
        #menu_items = self._get_category_source_menu_items()
        #active_source = self._model.get_active_category_source()
        #dropdown = Dropdown(label=active_source, menu=menu_items)
        #dropdown.on_change('value', new_category_source)

        update_value_callback = self._model.get_active_category_source
        update_options_callback = self._get_category_source_menu_items
        on_change_callback = new_category_source
        return DropdownWidget.init_dropdown_widget(update_value_callback,
                                                   update_options_callback,
                                                   on_change_callback)

    def init_color_method_radio(self):
        update_value_callback = self._model.get_active_color_method
        update_options_callback = self._model.get_available_color_methods
        on_change_callback = self._model.new_color_method_action

        return RadioWidget.init_radio_widget(update_value_callback, update_options_callback,
                                             on_change_callback)

    def init_point_label_radio(self):
        update_value_callback = self._model.get_point_label_visibility
        update_options_callback = self._model.get_point_label_options
        on_change_callback = self._model.new_point_label_visibility_action

        return RadioWidget.init_radio_widget(update_value_callback, update_options_callback,
                                             on_change_callback)

    def init_number_of_clusters_input(self):
        update_value_callback = lambda: int(self._model.get_number_of_clusters())
        on_change_callback = lambda attr, old, new:\
                             self._model.new_number_of_clusters_action(int(new))
        # LDA will not divide the space under n_components + 1 (n_components = 2)
        # Hence: start = 3; end = 7 (max number of colors for categories)
        return SliderWidget.init_slider_widget(update_value_callback, on_change_callback,
                                               title="Number of clusters", start=3,
                                               end=7, step=1)

    def init_initial_size_input(self):
        update_value_callback = lambda: int(self._model.get_initial_size())
        on_change_callback = lambda attr, old, new:\
                             self._model.new_initial_size_action(int(new))
        return SliderWidget.init_slider_widget(update_value_callback, on_change_callback,
                                               title="Initial size", start=1,
                                               end=40, step=1)

    def init_final_size_input(self):
        update_value_callback = lambda: int(self._model.get_final_size())
        on_change_callback = lambda attr, old, new:\
                             self._model.new_final_size_action(int(new))
        return SliderWidget.init_slider_widget(update_value_callback, on_change_callback,
                                               title="Final size", start=1,
                                               end=40, step=1)

    def init_view_name_input(self):
        value = self._model.get_active_view_alias()
        text_input = TextInput(title="New view:",
                               value=value)
        return text_input

    def get_upper_menu_layout(self):
        return self._upper_menu

    def get_upper_right_menu_layout(self):
        return self._upper_right_menu

    def get_lateral_menu_layout(self):
        return self._lateral_menu

    def _synchronize_classification(self):
        """Synchronize classification methods with sources"""
        self._classification_select.update_options()

    def _synchronize_sources(self):
        GeneralViewMenu.LOGGER.debug("Syncing sources")
        self._category_source_dropdown.menu = self._get_category_source_menu_items()

    def _get_category_source_menu_items(self):
        menu_items = []
        category_methods_mx = self._model.get_available_category_sources()
        for method_subset in category_methods_mx:
            menu_items += ([(method, method) for method in method_subset])
            menu_items.append(None)
        return menu_items
