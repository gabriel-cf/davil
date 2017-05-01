"""
    This script will launch the view for Star Coordinates on
    http://localhost:5006/starcoordinatesview
"""

from mymodule.frontend.model.general_model import GeneralModel

file_path = "cereal.csv"
model = GeneralModel.star_coordinates_init("SC", file_path)
