""" 
    Star Coordinates Mapper module
"""
import logging

class StarMapper():
    """Star class defining the methods for mapping points"""
    
    @staticmethod
    def map_points(dimensional_values_df, axis_vectors_df, weights_df=None,
                   normalized_weights=False, normalization_method=None):
        """ Map points according to Star Coordinates setting
            dimensional_values_df: pandas.Dataframe Values per axis per product
            axis_vectors_df: pandas.Dataframe Vector values per X, Y components
            weights_df: pandas.Dataframe Weight value per vector
            [normalized_weights=False]: If the weights should be normalized
            [normalization_method=None]: Normalization method for weights
        """
        # TODO - Add weights to the multiplication
        mapped_points = dimensional_values_df.dot(axis_vectors_df)
        mapped_points.columns = ['x', 'y']
        return mapped_points
