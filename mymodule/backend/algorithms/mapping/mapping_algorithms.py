""" 
    Star Coordinates Mapper module
"""
import logging
import random
import pandas as pd

class MappingAlgorithms():
    """Class holding the maping algorithms"""
    
    @staticmethod
    def dummy_coordinates(dimensional_values_df, axis_vectors_df, weights_df=None,
                          normalized_weights=False, normalization_method=None):
        """ Maps the points to random coordinates
            dimensional_values_df: pandas.DataFrame Values per axis per product
            axis_vectors_df: pandas.DataFrame Vector values per X, Y components
            weights_df: pandas.DataFrame Weight value per vector
            [normalized_weights=False]: If the weights should be normalized
            [normalization_method=None]: Normalization method for weights
        """
        min_range = -2
        max_range = 2   
        n_points = len(dimensional_values_df.index)
        x_l = [random.uniform(min_range, max_range) for i in xrange(0, n_points)]
        y_l = [random.uniform(min_range, max_range) for i in xrange(0, n_points)]
        name_l = dimensional_values_df.index.tolist()

        return pd.DataFrame({'x':x_l, 'y':y_l}, index=name_l)

    @staticmethod
    def star_coordinates(dimensional_values_df, axis_vectors_df, weights_df=None,
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

    #@staticmethod
    #def principal_component_biplot(dimensional_values_df, axis_vectors_df, weights_df=None,
    #                               normalized_weights=False, normalization_method=None):
    #    pass
    #    """ Map points according to Star Coordinates setting
    #        dimensional_values_df: pandas.Dataframe Values per axis per product
    #        axis_vectors_df: pandas.Dataframe Vector values per X, Y components
    #        weights_df: pandas.Dataframe Weight value per vector
    #        [normalized_weights=False]: If the weights should be normalized
    #        [normalization_method=None]: Normalization method for weights
    #    """