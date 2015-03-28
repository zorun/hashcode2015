import math
import sys
from collections import namedtuple


Point = namedtuple("Point", ("row", "col"))
Vector = namedtuple("Vector", ("drow", "dcol"))


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
