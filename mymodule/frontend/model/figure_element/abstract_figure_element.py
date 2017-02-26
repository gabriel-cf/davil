"""
    AbstractFigureElement
"""

from abc import ABCMeta, abstractmethod

class AbstractFigureElement(object):
    """Abstract figure element class that defines the methods to handle complex
       figure elements composed by sub-elements (like the segment and the 
       square that compose an axis) allowing to perform operations upon all
       children elements
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def visible(self, show):
        """Will mark as visible or invisible all children elements
           show: (Boolean)
        """

    @abstractmethod
    def get_identifier(self):
        """Will return the identifier of the element"""

    @abstractmethod
    def is_visible(self):
        """Will return True if the element is visible"""

