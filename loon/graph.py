from collections import namedtuple

import networkx as nx


Node = namedtuple("Node", "row", "col", "alt", "input")


class LoonGraph(object):
    """Graph structure: each position (row, col, alt) is modelled as two nodes
    (True → input, False → output)
    Input node: (row, col, alt, True)
    Output node: (row, col, alt, False)
    Sink: None
    """

    def __init__(self, loon):
        g = nx.DiGraph()
        # Source
        self.source = Node(row=loon.start_row, col=loon.start_col, alt=0, input=False)
        g.add_node(self.source)
        # Sink
        self.sink = None
        g.add_node(self.sink)
        for alt in range(1, loon.altitudes + 1):
            for row in range(loon.nb_rows):
                for col in range(loon.nb_cols):
                    n_in = Node(row, col, alt, True)
                    n_out = Node(row, col, alt, False)
                    g.add_node(n_in)
                    g.add_node(n_out)
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
                        g.add_edge(n_out, Node(row + vec.drow, (col + vec.dcol) % loon.nb_cols, alt, True)
        # Connect source to graph
        g.add_edge(self.source, Node(row=self.source.row, col=self.source.col, alt=1, input=True))
        self.g = g
