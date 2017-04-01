"""
    General Model
"""
from bokeh.io import curdoc
from handlers.view_menu_handler import ViewMenuHandler
from ...view.star_coordinates_view import StarCoordinatesView
from ...view.menu.general_view_menu import GeneralViewMenu
# Here we would set the rest of view imports

class GeneralModel(object):
    """docstring for GeneralModel"""
    def __init__(self, doc=None):
        self._doc = doc if doc else curdoc()        
        # Handler with the logic for adding and retrieving views and menus
        self._view_menu_handler = ViewMenuHandler()
        self._active_menu = None
        self._active_view = None
        self._active_view_root = None
        self._root = None

    def set_active_view(self, view_alias, set_doc_title=True):
        # TODO - doc-root logic to visualize the new view
        self._active_view = self._view_menu_handler.get_view_from_alias(view_alias)
        active_view_layout = self._active_view.get_layout()
        if self._active_view_root:
            print self._active_view_root
            #self._doc.remove_root(self._active_view_root)
            
            #self._doc.add_root(self._active_view_root)
            self._active_view_root.children[0] = active_view_layout
            self._active_view_root = self._active_view.get_layout()
        if set_doc_title:
            self._doc.title = view_alias

    def set_active_menu(self, menu_alias):
        menu = self._view_menu_handler.get_menu_from_alias(menu_alias)
        menu_layout = menu.get_layout()
        active_view_layout = self._active_view.get_layout()
        if self._root is None:
            self._root = menu_layout
            self._active_view_root = active_view_layout
            self._doc.add_root(self._root)
            self._doc.add_root(self._active_view_root)
            #self._root.children[1] = self._active_view.get_layout()
        else:
            old_root = self._root
            self._root.add_root(menu_layout)
            self._doc.add_root(active_view_layout)
            #self._root.children[1] = old_root.children[1]

        self._active_menu = menu

    def add_star_coordinates_view(self, alias, file, active=True):
        """Will generate a a new Star Coordinates view
           file: (String) path to the source file of the view
           [active=True]: set this view as the new active view
        """
        view = StarCoordinatesView(alias, file)
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
        file = new_file
        if not file:
            file = self._active_view.get_file()
        self.add_star_coordinates_view(alias, file)

    def new_reset_action(self):
        print "RESTARTING"
        self.reset_active_view()

    def new_mapping_select_action(self, new):
        print "Updating mapping algorithm to {}".format(new)
        self._active_view.update_mapping_algorithm(new)        

    def new_clustering_select_action(self, new):
        print "Updating clustering algorithm to {}".format(new)
        self._active_view.update_clustering_algorithm(new) 

    def new_error_select_action(self, new):
        print "Updating error algorithm to {}".format(new)
        self._active_view.update_error_algorithm(new)

    def new_file_select_action(self, new):
        print "Loading new file '{}'".format(new)        
        self.reset_active_view(new_file=new)

    def new_axis_checkbox_action(self, element_id, checked):
        """This function will be called every time a checkbox is checked
           Will hide or show the selected axis and remap the points
        """
        print "Updating axis visibility {};{}".format(element_id, checked)
        self._active_view.update_axis_visibility(element_id, checked)

    def new_initial_size_action(self, new):
        print "Updating initial size to {}".format(new)
        self._active_view.update_initial_size_input(new)

    def new_final_size_action(self, new):
        print "Updating final size to {}".format(new)
        self._active_view.update_final_size_input(new)    

    def new_table_action(self):
        print "NEW TABLE"

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

    def get_initial_size(self):
        return self._active_view.get_initial_size()

    def get_final_size(self):
        return self._active_view.get_final_size()
