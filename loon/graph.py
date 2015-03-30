from collections import namedtuple
import os.path
import itertools

import networkx as nx

import utils
from constants import GRAPH


Node = namedtuple("Node", ("row", "col", "alt", "input"))

class LoonGraph(object):
    """Graph structure: each position (row, col, alt) is modelled as two nodes
    (True → input, False → output)
    Input node: (row, col, alt, True)
    Output node: (row, col, alt, False)
    Sink: None
    """

    def __init__(self, loon):
        self.source = Node(row=loon.start_row, col=loon.start_col, alt=0, input=False)
        self.sink = None
        if os.path.exists(GRAPH):
            self.g = nx.read_gpickle(GRAPH)
        else:
            # Load graph from file if it is already computed
            self.build_graph(loon)
            nx.write_gpickle(self.g, GRAPH)

    def build_graph(self, loon):
        g = nx.DiGraph()
        # Source
        g.add_node(self.source)
        g.node[self.source]["nb_targets"] = 0
        # Sink
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
                        g.add_edge(n_in, Node(row, col, alt - 1, False))
                    if alt < loon.altitudes:
                        g.add_edge(n_in, Node(row, col, alt + 1, False))
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

        alt_moves = list()
        cyclic_list = itertools.cycle(cycle[1:])
        while next(cyclic_list) != start_Node:
            pass

        current_node = start_Node
        for hop in range(nb_hops):
            next_node = next(cyclic_list)
            if next_node.input == True: #skip the transition from input.False to input.True
                next_node = next(cyclic_list)

            alt_moves.append(next_node.row - current_node.row)
            current_node = next_node

        return alt_moves

    def path_to_movements(self, path):
        for (node1, node2) in zip(path, path[1:]):
            #print(node1, node2)
            if node1 == None or node2 == None:
                yield 0
            elif node2.alt > node1.alt:
                yield 1
            elif node2.alt < node1.alt:
                yield -1
            elif node1.input == True: #skip the transition from input.True to input.False
                continue
            elif node2.alt == node1.alt:
                yield 0

    def test(self, node):
        for neigh in self.g[node]:
            for e in utils.bfs_edges_limit(self.g, neigh, 15):
                print(e)

