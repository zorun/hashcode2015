from collections import namedtuple

import networkx as nx

import utils

import os.path

import pickle

Node = namedtuple("Node", ("row", "col", "alt", "input"))


class LoonGraph(object):
    """Graph structure: each position (row, col, alt) is modelled as two nodes
    (True → input, False → output)
    Input node: (row, col, alt, True)
    Output node: (row, col, alt, False)
    Sink: None
    """

    def __init__(self, loon):
        if os.path.exists('graph.gpickle'):
            
           # self = pickle.load(open('graph.txt'))
            self=nx.read_gpickle("graph.gpickle")
        else:
            self.build_graph(loon)
            nx.write_gpickle(self,"graph.gpickle")
            #pickle.dump(self, open('graph.txt', 'w'))
            # Load graph from file if it is already computed
            pass

    def build_graph(self, loon):
        g = nx.DiGraph()
        # Source
        self.source = Node(row=loon.start_row, col=loon.start_col, alt=0, input=False)
        g.add_node(self.source)
        g.node[self.source]["nb_targets"] = 0
        # Sink
        self.sink = None
        g.add_node(self.sink)
        g.node[self.sink]["nb_targets"] = 0
        for alt in range(1, loon.altitudes + 1):
            for row in range(loon.nb_rows):
                for col in range(loon.nb_cols):
                    n_in = Node(row, col, alt, True)
                    n_out = Node(row, col, alt, False)
                    g.add_node(n_in)
                    g.add_node(n_out)
                    g.add_edge(n_in, n_out)
                    # Link to other altitudes
                    if alt > 1:
                        g.add_edge(n_out, Node(row, col, alt - 1, True))
                    if alt < loon.altitudes:
                        g.add_edge(n_out, Node(row, col, alt + 1, True))
                    # Wind
                    vec = loon.winds[alt][row][col]
                    if row + vec.drow >= loon.nb_rows or row + vec.drow < 0:
                        # Ballon is lost
                        g.add_edge(n_out, self.sink)
                    else:
                        g.add_edge(n_out, Node(row + vec.drow, (col + vec.dcol) % loon.nb_cols, alt, True))
                    # Covered targets
                    here = utils.Point(row=row, col=col)
                    targets = [t for t in loon.targets if loon.is_in_range(here, t)]
                    #print("{} targets at position ({}, {}, {})".format(len(targets), alt, row, col))
                    g.node[n_in]["nb_targets"] = g.node[n_out]["nb_targets"] = len(targets)
        # Connect source to graph
        g.add_edge(self.source, Node(row=self.source.row, col=self.source.col, alt=1, input=True))
        self.g = g

#from input=False to input=True we print

    def get_movements(self, cycle, start_Node, balloon, nb_hops):
        for i in len(cycle):
            if cycle[i] == start_Node:
                break
        current_node = i
        next_node = current_node
        for hop in range(nb_hops):
            if current_node + 1 == len(cycle):
                next_node = 0
            else:
                next_node = next_node + 1
            pass