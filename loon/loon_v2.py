import sys
from collections import namedtuple

Point = namedtuple("Point", "row", "col", "alt")


class Loon(object):

    def __init__(self, input_file):

        self.targets = list()
        self.winds = list()

        with open(input_file) as f:
            self.nb_rows, self.nb_cols, self.altitudes = [int(x) for x in f.readline().split(' ')]
            self.nb_targets, self.radius, self.balloons, self.turns = [int(x) for x in f.readline().split(' ')]
            for i in range(self.nb_targets):
                self.targets.append([(int(x), int(y)) for (x,y) in f.readline().strip().split(' ')])
            for i in range(self.nb_rows*self.altitudes):
                self.winds.append(list(f.readline().strip()))

if __name__ == '__main__':
    k = range(0, 8, 1)
    l = Loon(sys.argv[1])

    # Test point
    p = Point(row=42, col=150, alt=5)
    print(p.alt)

    ##print(*i)
    for j in k:
        print(*([1]*53))
    for i in range(0, 392):
        print(*([0]*53))
