"""
    Line equation calculator
"""

import numpy as np

def calculate_line_equation(x0x1, y0y1):
    """Being the equation of the line: y = mx + c where m and c are
       constants, this method will return the (int) 'm' and 'c' constants
       Returns:
       'm': (int) calculated p constant for each point
       'c': (int) calculated c constant for each point
    """
    A = np.stack([x0x1, np.ones(len(x0x1))]).T
    m, c = np.linalg.lstsq(A, y0y1)[0]

    return m, c