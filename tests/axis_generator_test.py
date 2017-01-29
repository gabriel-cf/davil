"""
    Test AxisGenerator
"""
from ..mymodule.io.reader import Reader
from ..mymodule.util.axisgenerator import AxisGenerator

source_file = "C:/Users/gchicafernandez/Desktop/Personal/TFGs/Data Visualization/mymodule/resources/cereal_data_set/cereal.csv"

reader = Reader.init_from_file(source_file)
dimension_labels = reader.get_dimension_labels()
axis_df = AxisGenerator.generate_star_axis(dimension_labels, random_weights=True)

print axis_df
