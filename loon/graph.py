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
    - Input node: (row, col, alt, True)
    - Output node: (row, col, alt, False)
    - Sink: None

    Edges have a "weight" attribute: 1 means that an action is generated
    when a balloon takes this edge (either going up, down, or staying at
    the same altitude).  A weight of 0 means that this edge can be taken
    freely, it does not correspond to any movement in reality.
    """

    def __init__(self, loon):
        self.source = Node(row=loon.start_row, col=loon.start_col, alt=0, input=True)
        self.sink = None
        self.loon = loon
        if os.path.exists(GRAPH):
            # Load graph from file if it is already computed
            self.g = nx.read_gpickle(GRAPH)
        else:
            self.build_graph()
            nx.write_gpickle(self.g, GRAPH)

    def build_graph(self):
        g = nx.DiGraph()
        # Source
        g.add_node(self.source)
        g.node[self.source]["nb_targets"] = 0
        # Sink
        g.add_node(self.sink)
        g.node[self.sink]["nb_targets"] = 0
        for alt in range(1, self.loon.altitudes + 1):
            for row in range(self.loon.nb_rows):
                for col in range(self.loon.nb_cols):
                    n_in = Node(row, col, alt, True)
                    n_out = Node(row, col, alt, False)
                    g.add_node(n_in)
                    g.add_node(n_out)
                    g.add_edge(n_in, n_out, weight=0)
                    # Link to other altitudes
                    if alt > 1:
                        g.add_edge(n_in, Node(row, col, alt - 1, False), weight=1)
                    if alt < self.loon.altitudes:
                        g.add_edge(n_in, Node(row, col, alt + 1, False), weight=1)
                    # Wind
                    vec = self.loon.winds[alt][row][col]
                    if row + vec.drow >= self.loon.nb_rows or row + vec.drow < 0:
                        # Ballon is lost
                        g.add_edge(n_out, self.sink, weight=1)
                    else:
                        g.add_edge(n_out, Node(row + vec.drow, (col + vec.dcol) % self.loon.nb_cols, alt, True), weight=1)
                    # Covered targets
                    here = utils.Point(row=row, col=col)
                    targets = [t for t in self.loon.targets if self.loon.is_in_range(here, t)]
                    #print("{} targets at position ({}, {}, {})".format(len(targets), alt, row, col))
                    g.node[n_in]["nb_targets"] = g.node[n_out]["nb_targets"] = len(targets)
        # Connect source to graph
        g.add_edge(self.source, Node(row=self.source.row, col=self.source.col, alt=1, input=False), weight=1)
        # Self-edge on the source, to model the fact that we can wait before launching a balloon
        g.add_edge(self.source, self.source, weight=1)
        self.g = g

    def path_to_movements(self, path):
        for (node1, node2) in zip(path, path[1:]):
            if node1 == self.sink or node2 == self.sink:
                yield 0
            elif self.g[node1][node2]["weight"] == 0:
                continue
            elif node2.alt > node1.alt:
                yield 1
            elif node2.alt < node1.alt:
                yield -1
            else:
                yield 0

    def test(self, node):
        for neigh in self.g[node]:
            for e in utils.bfs_edges_limit(self.g, neigh, 15):
                print(e)

