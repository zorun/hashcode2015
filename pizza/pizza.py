
import sys


class Part(object):

    def __init__(self, row1, col1, row2, col2):
        self.row1, self.col1, self.row2, self.col2 = row1, col1, row2, col2 


class Pizza(object):

    def __init__(self, input_file):
        # list of list of ('T' | 'H')
        self.pizza = list()
        # list of Part
        self.parts = list()
        with open(input_file) as f:
            self.nb_lines, self.nb_cols, self.min_ham, self.max_size = [int(x) for x in f.readline().split(' ')]
            for i in range(self.nb_lines):
                self.pizza.append(f.readline().strip().split(' '))

    def __str__(self):
        return "\n".join(["".join(row) for row in self.pizza])


if __name__ == '__main__':
    p = Pizza(sys.argv[1])
    print(p)
