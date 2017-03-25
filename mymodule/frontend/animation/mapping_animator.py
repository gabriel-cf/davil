from __future__ import division
import time
import pandas as pd
import numpy as np

class MappingAnimator(object):
    """Object that creates animations between two positions for points"""

    def __init__(self, source_points=None):
        """source_points: (ColumnDataSource) source where to update the values
        """
        self._source_points = source_points

    def add_source_points(self, source_points):
        self._source_points = source_points

    def step_x_exponential(self, step_points_df, final_points, step, total_steps):
        #next_x_values = []
        for i in xrange(0, len(step_points_df['x'])):
            x0 = step_points_df['x'][i]
            xf = final_points['x'][i]
            step_points_df['x'][i] = x0 + step * (xf - x0) / total_steps
            #next_x_values.append(xi)
        #print next_x_values
        #s = pd.Series(next_x_values)
        #step_points_df['x'] = s
        return step_points_df

    def step_x_constant(self, original_points, step_points_df, final_points, step, total_steps):
        #next_x_values = []
        for i in xrange(0, len(original_points['x'])):
            x0 = original_points['x'][i]
            xf = final_points['x'][i]
            step_points_df['x'][i] = x0 + step * (xf - x0) / total_steps
            #next_x_values.append(xi)
        #print next_x_values
        #s = pd.Series(next_x_values)
        #step_points_df['x'] = s
        return step_points_df

    def evaluate_y(self, points_df, formula):
        points_df.eval('y = {}'.format(formula), inplace=True)

    def calculate_time_cost(self, points_df, mapped_points, formula, source_points):
        start_time = time.time()
        self.step_x_exponential(points_df, mapped_points, 0, 1)
        self.evaluate_y(points_df, formula)            
        source_points.data['x'] = points_df['x']
        source_points.data['y'] = points_df['y']
        end_time = time.time()
        time_cost = end_time - start_time
        print "TIME COST: {}s".format(time_cost)
        print "Freq: {}s".format(1/time_cost)
        return time_cost

    def get_animation_sequence(self, original_points, mapped_points, max_time=1.5):
        """Will map the points for every step of the sequence by updating
           the source

           original_points: (pandas.Dataframe) position of the points before
           mapped_points: (pandas.Dataframe) final position of the points
        """                

        # First, we get the cost time by simulating an animation from P0 to P'0
        # where P'0 has the same coordinates (this way we include the 
        # rendering time without modifying the position)
        step_points_cp, formula = self._get_equation_dataframe(original_points, mapped_points)
        time_cost = self.calculate_time_cost(step_points_cp, mapped_points, formula, self._source_points)
        total_steps = int(max_time // time_cost)
        print "TOTAL STEPS: {}".format(total_steps)
        for step in xrange(0, total_steps):
            #print step_points_cp['x']
            self.step_x_exponential(step_points_cp, mapped_points, step, total_steps)
            self.evaluate_y(step_points_cp, formula)            
            self._source_points.data['x'] = step_points_cp['x']
            self._source_points.data['y'] = step_points_cp['y']
        print "FINISHED ANIMATION"
                
            #print step_points_cp['x']
            #print step_points_cp['y']

        self._source_points.data['x'] = mapped_points['x']
        self._source_points.data['y'] = mapped_points['y']

        #start_time = time.time()
        #end_time = time.time()

    def _get_equation_dataframe(self, original_points, mapped_points):
        """Being the equation of the line: y = mx + c where m and c are
           constants, this method will return a dataframe composed by the
           following columns:
           'x': x points (with values as per original_points df)
           'm': calculated p constant for each point
           'c': calculated c constant for each point
           'y': equation 'mx + c'
        """
        formula = 'm * x + c'
        original_points_cp = original_points.copy()
        x_coords = zip(original_points['x'], mapped_points['x'])
        y_coords = zip(original_points['y'], mapped_points['y'])
        points = zip(x_coords, y_coords)
        m_l = []
        c_l = []
        for x0x1, y0y1 in points:
            A = np.stack([x0x1, np.ones(len(x0x1))]).T
            m, c = np.linalg.lstsq(A, y0y1)[0]
            m_l.append(m)
            c_l.append(c)        
        original_points_cp['m'] = pd.Series(m_l, index=original_points_cp.index)
        original_points_cp['c'] = pd.Series(c_l, index=original_points_cp.index)


        return original_points_cp, formula
