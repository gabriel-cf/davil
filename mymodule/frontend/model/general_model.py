"""
    General Model
"""
import logging
from bokeh.io import curdoc
from bokeh.layouts import row, column
from .handlers.view_menu_handler import ViewMenuHandler
from ..view.star_coordinates_view import StarCoordinatesView
from ..menu.general_view_menu import GeneralViewMenu
from ..menu.checkboxgroup_widget import CheckboxGroupWidget
from ..menu.table_generator import TableGenerator
# Here we would set the rest of view imports

class GeneralModel(object):
    """docstring for GeneralModel"""
    LOGGER = logging.getLogger(__name__)

    @staticmethod
    def star_coordinates_init(alias, file, doc=None):
        model = GeneralModel(doc=doc)
        model.add_star_coordinates_view(alias, file)
        model.add_general_menu(alias)
        model.init_layouts()
        return model

    def __init__(self, doc=None):
        self._doc = doc if doc else curdoc()        
        # Handler with the logic for adding and retrieving views and menus
        self._view_menu_handler = ViewMenuHandler()
        self._active_root = None
        self._active_menu = None
        self._active_view = None

    def add_star_coordinates_view(self, alias, file, active=True):
        """Will generate a a new Star Coordinates view
           file: (String) path to the source file of the view
           [active=True]: set this view as the new active view
        """
        view = StarCoordinatesView(alias, file)
        checkboxgroup = CheckboxGroupWidget(view)
        table = TableGenerator.init_table(view)
        view.set_checkboxes(checkboxgroup)
        view.set_table(table)
        self._view_menu_handler.add_view(alias, view)
        if active:
            self.set_active_view(alias)

    def add_general_menu(self, alias, active=True):
        """Will generate a a new GeneralViewMenu
           [active=True]: set this menu as the new active menu
        """
        menu = GeneralViewMenu(self)
        self._view_menu_handler.add_menu(alias, menu)
        if active:
            self.set_active_menu(alias)

    def reset_active_view(self, new_file=None):
        # TODO - find a way to destroy the current view
        alias = self._active_view.get_alias()
        self._view_menu_handler.remove_view(alias)
        file_ = new_file
        if not file_:
            file_ = self._active_view.get_file()
        self.add_star_coordinates_view(alias, file_)

    def init_layouts(self):
        GeneralModel.LOGGER.debug("Generating layouts")
        layout = self._get_layout()
        if not self._active_root:
            self._active_root = layout
            self._doc.add_root(layout)
        else:
            self._update_checkboxes_layout(self._active_view)
            self._update_view_layout(self._active_view)            

    def set_active_view(self, view_alias):
        new_view = self._view_menu_handler.get_view_from_alias(view_alias)
        # We need to redraw the view, otherwise bokeh won't visualize it
        new_view.redraw()
        self._active_view = new_view
        GeneralModel.LOGGER.info("Active view set to '%s'", view_alias)
        # Synchronize the new view with the values of the menu
        if self._active_menu:
            self._active_menu.synchronize_view()

    def set_active_menu(self, menu_alias):
        self._active_menu = self._view_menu_handler.get_menu_from_alias(menu_alias)

    def _update_view_layout(self, new_view):
        layout = curdoc().get_model_by_name('view')
        layout.children = new_view.get_layout().children

    def _update_checkboxes_layout(self, new_view):
        layout = curdoc().get_model_by_name('checkboxes')
        layout.children = new_view.get_checkboxes_layout().children
  
    def _get_layout(self):
        return row(self._active_menu.get_lateral_menu_layout(),
                   column(self._active_menu.get_upper_menu_layout(),
                          self._active_view.get_layout()),
                   column(self._active_menu.get_upper_right_menu_layout(),
                          self._active_view.get_checkboxes_layout()), 
                   self._active_menu._right_menu, name='main_layout')

    def new_add_view_action(self, name=None):
        name = name
        filename = self._active_view.get_file()
        get_unique_name = lambda name: "{}_{}".format(name,
                                      len(self._view_menu_handler.get_available_views()))
        if not name:
            name = get_unique_name(filename)
        elif self._view_menu_handler.has_view_alias(name):
            name = get_unique_name(name)
        GeneralModel.LOGGER.info("Adding new view '%s'", name)
        self.add_star_coordinates_view(name, filename)
        self.init_layouts()
        return name

    def new_mapping_select_action(self, new):
        GeneralModel.LOGGER.info("Updating mapping algorithm to '%s'", new)
        self._active_view.update_mapping_algorithm(new)

    def new_normalization_select_action(self, new):
        GeneralModel.LOGGER.info("Updating normalization algorithm to '%s'", new)
        self._active_view.update_normalization_algorithm(new)

    def new_clustering_select_action(self, new):
        GeneralModel.LOGGER.info("Updating clustering algorithm to '%s'", new)
        self._active_view.update_clustering_algorithm(new)

    def new_error_select_action(self, new):
        GeneralModel.LOGGER.info("Updating error algorithm to '%s'", new)
        self._active_view.update_error_algorithm(new)

    def new_axis_select_action(self, new):
        GeneralModel.LOGGER.info("Selecting axis '%s'", new)
        self._active_view.update_selected_axis(new)

    def new_category_source_select_action(self, new):
        GeneralModel.LOGGER.info("Selecting category source '%s'", new)
        self._active_view.update_selected_category_source(new)

    def new_color_method_select(self, new): 
        GeneralModel.LOGGER.info("Updating coloring method to '%s'", new)
        self._active_view.update_color_method(new)

    def new_palette_select_action(self, new):
        GeneralModel.LOGGER.info("Coloring using palette '%s'", new)
        self._active_view.update_palette(new)

    def new_file_select_action(self, filename):
        GeneralModel.LOGGER.info("Loading new file '%s'", filename)
        self.reset_active_view(filename)
        self.init_layouts()

    def new_classification_action(self, new):
        GeneralModel.LOGGER.info("Classifying with '%s'", new)
        self._active_view.update_classification_algorithm(new)

    def new_view_select_action(self, alias):
        GeneralModel.LOGGER.info("Setting active view: '%s'", alias)
        view = self._view_menu_handler.get_view_from_alias(alias)
        # If there is already a view for that file
        if view:
            self.set_active_view(alias)
        self.init_layouts()

    def new_number_of_clusters_action(self, new):
        self._active_view.update_number_of_clusters(new)

    def new_initial_size_action(self, new):
        self._active_view.update_initial_size_input(new)

    def new_final_size_action(self, new):
        self._active_view.update_final_size_input(new)

    def new_color_method_action(self, new):
        GeneralModel.LOGGER.info("Setting color method to: '%s'", new)
        self._active_view.update_color_method(new)

    def new_point_label_visibility_action(self, new):
        GeneralModel.LOGGER.info("Setting labels visibility to: '%s'", new)
        self._active_view.update_point_label_visibility(new)

    ######################################################################

    def get_axis_status(self):
        """Calls the get_axis_status method of the active view
           Must return a zipped list of [(axis_id, visible), ..]
        """
        axis_status = self._active_view.get_axis_status()
        return axis_status

    def get_mapping_algorithm(self):
        return self._active_view.get_mapping_algorithm()

    def get_mapping_options(self):
        return self._active_view.get_mapping_options()

    def get_normalization_algorithm(self):
        return self._active_view.get_normalization_algorithm()

    def get_normalization_options(self):
        return self._active_view.get_normalization_options()

    def get_clustering_algorithm(self):
        return self._active_view.get_clustering_algorithm()

    def get_clustering_options(self):
        return self._active_view.get_clustering_options()

    def get_error_algorithm(self):
        return self._active_view.get_error_algorithm()

    def get_error_options(self):
        return self._active_view.get_error_options()

    def get_file(self):
        return self._active_view.get_file()

    def get_available_files(self):
        return self._active_view.get_available_files()

    def get_classification_algorithm(self):
        return self._active_view.get_classification_algorithm()

    def get_classification_methods(self):
        return self._active_view.get_classification_methods()

    def get_selected_axis_id(self):
        return self._active_view.get_selected_axis_id()

    def get_available_axis_ids(self):
        return self._active_view.get_available_axis_ids()

    def get_available_palettes(self):
        return self._active_view.get_available_palettes()

    def get_palette(self):
        return self._active_view.get_palette()

    def get_active_color_method(self):
        return self._active_view.get_active_color_method()

    def get_available_color_methods(self):
        return self._active_view.get_available_color_methods()

    def get_available_category_sources(self):
        return self._active_view.get_available_category_sources()

    def get_active_category_source(self):
        return self._active_view.get_active_category_source()

    def get_active_view_alias(self):
        return self._active_view.get_alias()

    def get_available_views(self):
        return self._view_menu_handler.get_available_views()

    def get_number_of_clusters(self):
        return self._active_view.get_number_of_clusters()

    def get_initial_size(self):
        return self._active_view.get_initial_size()

    def get_final_size(self):
        return self._active_view.get_final_size()

    def get_point_label_visibility(self):
        return self._active_view.get_point_label_visibility()

    def get_point_label_options(self):
        return self._active_view.get_point_label_options()
