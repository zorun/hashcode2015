import sys
import math
import pickle

import utils
from utils import Point, Vector
from graph import LoonGraph



class Loon(object):

    def __init__(self, input_file):

        self.targets = list()
        self.winds = dict()

        with open(input_file) as f:
            self.nb_rows, self.nb_cols, self.altitudes = [int(x) for x in f.readline().split(' ')]
            self.nb_targets, self.radius, self.balloons, self.turns = [int(x) for x in f.readline().split(' ')]
            self.start_row, self.start_col = [int(x) for x in f.readline().split(' ')]

            for i in range(self.nb_targets):
                x, y = f.readline().strip().split(' ')
                self.targets.append(Point(row=int(x), col=int(y)))

            for alt in range(1,self.altitudes+1):
                self.winds[alt] = list()
                for row in range(self.nb_rows):
                    list_altitude = f.readline().strip().split(' ')
                    couple_wind = zip(list_altitude[::2],list_altitude[1::2])
                    self.winds[alt].append([Vector(drow=int(x), dcol=int(y)) for (col, (x, y)) in enumerate(couple_wind)])
        self.graph = LoonGraph(self)    
        



    def is_in_range(self, point1, point2):
        dcol = abs(point2.col - point1.col)
        drow = abs(point2.row - point1.row)
        columndist = min(dcol, self.nb_cols - dcol)
        return (drow * drow + columndist * columndist <= self.radius * self.radius)


if __name__ == '__main__':
    k = range(0, 8, 1)
    l = Loon(sys.argv[1])

    # Test point
    p = Point(row=42, col=150)
    #print(p.alt)


