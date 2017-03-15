"""
    This script will launch the view for Star Coordinates on
    http://localhost:5006/starcoordinatesview
"""

from mymodule.view.star_coordinates_view import StarCoordinatesView

file_path = "mymodule/resources/main.csv"
StarCoordinatesView(file_path).init()
