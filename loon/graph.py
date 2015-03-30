from collections import namedtuple
import os.path
import itertools

import networkx as nx

import utils
from constants import GRAPH


Node = namedtuple("Node", ("row", "col", "alt", "input"))


# This is used to mark nodes when exploring the graph with BFS:
# - last_time: time of the last exploration of this node
# - total_score: cumulated score of the current best path from starting node to this node
# - ancestor: previous node in the current best path from starting node to this node
Mark = namedtuple("Mark", ("last_time", "total_score", "ancestor"))


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

    def bfs_edges(self, start_node, limit=400):
        """Produce edges in a breadth-first-search starting at source.
        Modified from networkx to limit to a given distance from the source"""
        def add_mark(node, mark):
            self.g.node[node]["mark"] = mark

        add_mark(start_node, Mark(0, 0, None))
        stack = [(start_node, 0, iter(self.g[start_node]))]
        while stack:
            parent, dist, children = stack[0]
            if dist >= limit:
                stack.pop(0)
            else:
                try:
                    child = next(children)
                    weight = self.g[parent][child].get("weight", 1)
                    # We multiply by the weight, so that 0-weight edges don't increase the score
                    child_score = self.g.node[parent]["mark"].total_score + weight * self.g.node[child]["nb_targets"]
                    # Either we haven't visited the child yet, or we found a better path
                    if ("mark" not in self.g.node[child]) or (child_score > self.g.node[child]["mark"].total_score):
                        add_mark(child, Mark(self.g.node[parent]["mark"].last_time + weight, child_score, parent))
                        yield parent, child
                        stack.append((child, dist + weight, iter(self.g[child])))
                except StopIteration:
                    stack.pop(0)

    def test(self, node, limit=10):
        best_node = node
        for e in self.bfs_edges(node, limit):
            mark = self.g.node[e[1]]["mark"]
            print(e[1], mark)
            if mark.last_time == limit:
                best_node = max(best_node, e[1], key=lambda n: self.g.node[n]["mark"].total_score)
        print("Best: {} with score {}".format(best_node, self.g.node[best_node]["mark"].total_score))
