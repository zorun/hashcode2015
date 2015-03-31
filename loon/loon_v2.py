import sys
import math
import pickle
import random

import utils
from utils import Point, Vector
from graph import LoonGraph



class Loon(object):

    def __init__(self, input_file, output_file):
        self.output_file = output_file

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

    def build_graph(self):
        self.graph = LoonGraph(self)

    def print_wind(self, altitude):
        # Print the map with a rotation of 90°, so that it fits on a 80-column terminal
        for col in range(self.nb_cols):
            for row in range(self.nb_rows):
                print(utils.get_wind(self.winds[altitude][row][col]), end='')
            print()

    def is_in_range(self, point1, point2):
        dcol = abs(point2.col - point1.col)
        drow = abs(point2.row - point1.row)
        columndist = min(dcol, self.nb_cols - dcol)
        return (drow * drow + columndist * columndist <= self.radius * self.radius)

    def get_movements(self, ballon):
        # Bruteforce by increments (18 edges for the first bruteforce,
        # then 15 for all the following ones, see below)
        limit = 18
        node = self.graph.source
        path = [node]
        while len(path) < self.turns + 1:
            score, res = self.graph.bruteforce(node, min(limit, self.turns + 1 - len(path)))
            limit = 15
            res.reverse()
            path.extend(res[1:])
            node = res[-1]
        return list(self.graph.path_to_movements(path))

    def solve(self):
        moves = [self.get_movements(0)] * self.balloons
        self.print_loon(moves)

    def print_loon(self, events):
        f = open(self.output_file, "w")
        for i in range(0, self.turns):
            for j in range(0, self.balloons):
                f.write("{} ".format(events[j][i]))
            f.write("\n")
        f.close()


if __name__ == '__main__':
    out = sys.argv[2] if len(sys.argv) > 2 else "loon.out"
    l = Loon(sys.argv[1], out)
    #l.print_wind(5)
    l.build_graph()
    #l.graph.display_graph()
    #l.graph.test(l.graph.source)
    #l.graph.test_bruteforce()
    l.solve()
