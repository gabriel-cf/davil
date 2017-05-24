"""
    Test StarMapper
"""
from ..mymodule.model.mapper.starmapper import StarMapper
from ..mymodule.io.reader import Reader
from ..mymodule.util.axisgenerator import AxisGenerator
from ..mymodule.util.dfmatrixutils import DFMatrixUtils

source_file = "C:/Users/gchicafernandez/Desktop/Personal/TFGs/Data Visualization/mymodule/resources/cereal_data_set/cereal.csv"

reader = Reader.init_from_file(source_file)
dimension_values_df = reader.get_dimension_values()
dimension_labels = reader.get_dimension_labels()
axis_df = AxisGenerator.generate_star_axis(dimension_labels, random_weights=True)



vectors_df = DFMatrixUtils.get_vectors(axis_df)

print vectors_df
print dimension_values_df

mapper = StarMapper()
print mapper.map_points(vectors_df, dimension_values_df)
