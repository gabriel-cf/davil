"""
    View and Menu Handler
"""

class ViewMenuHandler(object):
    """This class holds dictionaries and methods storing references
       to available axis and menu items. This architecture allows
       for the easy swapping between menus or views from the model
    """
    @staticmethod
    def _get_from_alias(alias, alias_dict):
        if alias in alias_dict:
            return alias_dict[alias]
        return None
        #raise ValueError("No element could not be found with given alias '{}'".format(alias))

    @staticmethod
    def _add_with_alias(alias, alias_dict, element, override=False):
        if alias in alias_dict:
            if not override:
                raise ValueError("Alias '{}' already present in dictionary".format(alias))
        alias_dict[alias] = element

    @staticmethod
    def _remove_alias(alias, alias_dict):
        """Remove from the menu dictionary the given alias
           It will only log if the alias is not found
        """
        if not alias in alias_dict:
            print "Alias '{}' not found while trying to remove it".format(alias)
        alias_dict.pop(alias, None)

    def __init__(self):
        self._menus = dict()
        self._views = dict()
        # Should we track here the active menu/view?
    
    def get_menu_from_alias(self, alias):
        return ViewMenuHandler._get_from_alias(alias, self._menus)

    def get_view_from_alias(self, alias):
        return ViewMenuHandler._get_from_alias(alias, self._views)

    def add_menu(self, alias, menu, override=False):
        # TODO: Control type
        ViewMenuHandler._add_with_alias(alias, self._menus, menu, override=override)

    def add_view(self, alias, view, override=False):
        # TODO: Control type
        ViewMenuHandler._add_with_alias(alias, self._views, view, override=override)

    def remove_menu(self, alias):
        ViewMenuHandler._remove_alias(alias, self._menus)

    def remove_view(self, alias):
        ViewMenuHandler._remove_alias(alias, self._views)

    def get_available_views(self):
        return self._views.keys()
    
    def get_available_menus(self):
        return self._menus.keys()