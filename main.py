"""
    This script will launch the view for Star Coordinates on
    http://localhost:5006/starcoordinatesview
"""

from mymodule.view.star_coordinates_view import StarCoordinatesView

file_path = "mymodule/resources/cereal_data_set/cereal.csv"
#file_path = "mymodule/resources/titanic_survivors.csv"
StarCoordinatesView(file_path).init()
