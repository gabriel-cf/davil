"""
    This script will launch the view for Star Coordinates on
    http://localhost:5006/starcoordinatesview
"""

from mymodule.views.starcoordinatesview import StarCoordinatesView

file_path = "mymodule/resources/cereal_data_set/cereal.csv"
view = StarCoordinatesView(file_path)

view.run()
