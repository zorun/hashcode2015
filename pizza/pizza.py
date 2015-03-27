
import sys


class Part(object):

    def __init__(self, pizza, row1, col1, row2, col2):
        self.row1 = min(row1, row2)
        self.row2 = max(row1, row2)
        self.col1 = min(col1, col2)
        self.col2 = max(col1, col2)
        self.size = (self.row2 - self.row1 + 1) * (self.col2 - self.col1 + 1)
        # Compute number of hams
        self.nb_hams = 0
        for i in range(row1, row2 + 1):
            for j in range(col1, col2 + 1):
                if pizza.pizza[i][j] == 'H':
                    self.nb_hams += 1

    def is_valid(self, min_ham, max_size):
        area = (abs(self.col1-self.col2)+1)*(abs(self.row1-self.row2)+1)
        if self.nb_hams >= min_ham and max_size >= area:
            return True
        else:
            return False

    def intersects(self, other):
        """Untested"""
        return other.row1 <= self.row2 and other.row2 >= self.row1 and other.col1 <= self.col2 and other.col2 >= self.col1


class Pizza(object):

    def __init__(self, input_file):
        # list of list of ('T' | 'H')
        self.pizza = list()
        # list of Part
        self.parts = list()
        with open(input_file) as f:
            self.nb_lines, self.nb_cols, self.min_ham, self.max_size = [int(x) for x in f.readline().split(' ')]
            for i in range(self.nb_lines):
                self.pizza.append(list(f.readline().strip()))

    def add_part(self, part):
        self.parts.append(part)

    def is_part_possible_size(self, part):
        return part.size <= self.max_size

    def is_part_possible_ham(self, part):
        return part.nb_hams >= self.min_ham

    def is_part_possible_collision(self, part):
        for p in self.parts:
            if part.intersects(p):
                return False
        return True

    def cut(self):
        for i in range(0, self. nb_lines-1):
            for j in range(0, self.nb_cols):
                if self.pizza[i][j] == 'H':
                    for t in range(0, self.max_size//2):
                        if t+j < self.nb_cols:
                            possible_part = Part(self, i, j, i+1, j+t)
                            if possible_part.is_valid(self.min_ham, self.max_size):
                                self.parts.append(possible_part)
                                for x in range(i,i+2):
                                    for y in range(j,j+t+1):
                                        self.pizza[x][y] = 'X'


    def is_part_possible(self, part):
        return self.is_part_possible_size(part) and self.is_part_possible_ham(part) and self.is_part_possible_collision(part)
    
    def __str__(self):
        return "\n".join(["".join(row) for row in self.pizza])

    def print_all(self):
        print(len(self.parts))
        for p in self.parts:
            print(p.row1, p.col1, p.row2, p.col2)
        
        return    

if __name__ == '__main__':
    p = Pizza(sys.argv[1])
    print(p.nb_lines, p.nb_cols)
    #part = Part(p.pizza, 3, 4, 4, 10)
    p.cut()
    #p.add_part(part)

    p.print_all()
