import math
import sys

def coverage(r, c, u, v, max_col, ran):
    columndist = min(math.fabs(c - v), max_col - math.fabs(c - v))
    return (math.pow((r - u), 2) + math.pow(columndist, 2) <= math.pow(ran,2))


def print_wind(r, c):


    s1 = "/>"
    s2 = "->"
    s3 = "\>"
    s4 = "|,"
    s5 = "|'"
    s6 = "</"
    s7 = "<-"
    s8 = "<\\"

    if (c > 0):
        if (r < 0):
            print(s1, end=' ')
            return
        if (r == 0):
            print(s2, end=' ')
            return
        if (r > 0):
            print(s3, end=' ')
            return
    if (c == 0):
        if (r < 0):
            print(s5, end=' ')
            return
        if (r > 0):
            print(s4, end=' ')
            return
    if (c < 0):
        if (r < 0):
            print(s8, end=' ')
            return
        if (r == 0):
            print(s7, end=' ')
            return
        if (r > 0):
            print(s6, end=' ')
            return
    return
