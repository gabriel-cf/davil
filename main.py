"""
    This script will launch the view for Star Coordinates on
    http://localhost:5006/starcoordinatesview
"""

from mymodule.frontend.model.general_model import GeneralModel

file_path = "mymodule/resources/main.csv"
model = GeneralModel()
model.add_star_coordinates_view("SC", file_path)
model.add_general_menu("SC")
