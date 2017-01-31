""" Axis Generator Module
"""
from __future__ import division
import random
from math import cos, sin, radians
import pandas as pd
import numpy as np

class AxisGenerator(object):
    """Static class with methods to generate DataFrames representing axis"""

    @staticmethod
    def _subdivide_circle(centre, n_lines):
        segment_list = []
        for i in xrange(0, n_lines):
            angle = radians(i * (360/n_lines))
            x0, y0 = centre
            cos_ = cos(angle)
            sin_ = sin(angle)
            # Float problem: cos(90), sin(180) != 0.0
            if abs(cos_) < 0.000000001:
                cos_ = 0
            if abs(sin_) < 0.000000001:
                sin_ = 0
            r = random.uniform(1, 3) ##
            x1 = x0 + r * cos_
            y1 = y0 + r * sin_
            segment = [x0, x1, y0, y1]
            segment_list.append(segment)
        
        return segment_list

    @staticmethod
    def _generate_weights(no_weights, random_weights=False):
        if random_weights:
            return np.random.rand(no_weights)
        return np.zeros(no_weights)

    @staticmethod
    def generate_star_axis(axis_labels, random_weights=True):
        no_axis = len(axis_labels)
        segment_list = AxisGenerator._subdivide_circle((0,0), no_axis)
        df = pd.DataFrame(segment_list, axis_labels, columns=["x0", "x1", "y0", "y1"])
        # Add weights
        weights = AxisGenerator._generate_weights(no_axis, random_weights)
        df['weight'] = pd.Series(weights, index=df.index)
        return df
        