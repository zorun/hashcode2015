import math
import sys

def coverage(r, c, u, v, max_col, ran):
    columndist = min(math.fabs(c - v), max_col - math.fabs(c - v))
    return (math.pow((r - u), 2) + math.pow(columndist, 2) <= math.pow(ran,2))
