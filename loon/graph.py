from collections import namedtuple
import os.path
import itertools

import networkx as nx

import utils
from constants import GRAPH


Node = namedtuple("Node", ("row", "col", "alt"))


# This is used to mark nodes when exploring the graph with BFS:
# - last_time: time of the last exploration of this node
# - total_score: cumulated score of the current best path from starting node to this node
# - ancestor: previous node in the current best path from starting node to this node
Mark = namedtuple("Mark", ("last_time", "total_score", "ancestor"))


class LoonGraph(object):
    """Graph structure: each position (row, col, alt) is a node of the graph.
    There is a sink, represented by None, which corresponds to going out
    of the map.
    """

    def __init__(self, loon):
        self.source = Node(row=loon.start_row, col=loon.start_col, alt=0)
        self.sink = None
        self.loon = loon
        if os.path.exists(GRAPH):
            # Load graph from file if it is already computed
            self.g = nx.read_gpickle(GRAPH)
        else:
            self.build_graph()
            nx.write_gpickle(self.g, GRAPH)
        # Pre-compute scores (3D list: row, col, time)
        self.scores = list()
        for row in range(self.loon.nb_rows):
            row_scores = list()
            for col in range(self.loon.nb_cols):
                row_scores.append([self.g.node[Node(row, col, 1)]["nb_targets"]] * self.loon.turns)
            self.scores.append(row_scores)

    def add_wind_edge(self, source, dest):
        """Adds an edge to the graph, from the given node [source], to the node
        obtained by following the wind from the [dest] node.

        Use dest == source to add a simple wind edge.
        """
        vec = self.loon.winds[dest.alt][dest.row][dest.col]
        if dest.row + vec.drow >= self.loon.nb_rows or dest.row + vec.drow < 0:
            # Ballon is lost
            wind_dest = self.sink
        else:
            wind_dest = Node(dest.row + vec.drow, (dest.col + vec.dcol) % self.loon.nb_cols, dest.alt)
        self.g.add_edge(source, wind_dest)

    def score(self, node, time):
        if node == self.sink:
            # Average score achievable per balloon per turn
            return -33
        if node.alt == 0:
            return 0
        return self.scores[node.row][node.col][time]

    def add_path(self, path):
        """Changes the score by marking visited nodes as not contributing to the
        score anymore"""
        for (time, node) in enumerate(path[1:]):
            if node == self.sink:
                continue
            position = utils.Point(node.row, node.col)
            # Optimisation attempt
            targets = [t for t in self.loon.targets if self.loon.is_in_range(position, t, 3 * self.loon.radius)]
            # Mark targets as covered
            for target in targets:
                if self.loon.is_in_range(position, target):
                    #print("Marking target {} as covered by node {} at time {}".format(target, node, time))
                    self.loon.targets[target][time] = True
            # Recompute score of neighbouring positions
            for row in range(node.row - 2 * self.loon.radius, node.row + 2 * self.loon.radius + 1):
                if row < 0 or row >= self.loon.nb_rows:
                    continue
                for col in range(node.col - 2 * self.loon.radius, node.col + 2 * self.loon.radius + 1):
                    col %= self.loon.nb_cols
                    point = utils.Point(row, col)
                    if self.loon.is_in_range(position, point, 2 * self.loon.radius):
                        self.scores[row][col][time] = len([target for target in targets if not self.loon.targets[target][time] and self.loon.is_in_range(point, target)])
                        #print("Score at point ({}, {}), time {}, is now {}".format(row, col, time, self.scores[row][col][time]))

    def build_graph(self):
        self.g = nx.DiGraph()
        # Source
        self.g.add_node(self.source)
        self.g.node[self.source]["nb_targets"] = 0
        # Sink
        self.g.add_node(self.sink)
        self.g.node[self.sink]["nb_targets"] = 0
        for alt in range(1, self.loon.altitudes + 1):
            for row in range(self.loon.nb_rows):
                for col in range(self.loon.nb_cols):
                    n = Node(row, col, alt)
                    self.g.add_node(n)
                    # Link to the same altitude (wind)
                    self.add_wind_edge(n, n)
                    # Link to other altitudes (change altitude + wind)
                    if alt > 1:
                        self.add_wind_edge(n, Node(row, col, alt - 1))
                    if alt < self.loon.altitudes:
                        self.add_wind_edge(n, Node(row, col, alt + 1))
                    # Covered targets
                    here = utils.Point(row=row, col=col)
                    targets = [t for t in self.loon.targets if self.loon.is_in_range(here, t)]
                    #print("{} targets at position ({}, {}, {})".format(len(targets), alt, row, col))
                    self.g.node[n]["nb_targets"] = len(targets)
        # Connect source to graph
        self.add_wind_edge(self.source, Node(row=self.source.row, col=self.source.col, alt=1))
        # Self-edge on the source, to model the fact that we can wait before launching a balloon
        self.g.add_edge(self.source, self.source)
        # Self-edge on the sink, to have a path of the right length
        self.g.add_edge(self.sink, self.sink)

    def path_to_movements(self, path):
        for (node1, node2) in zip(path, path[1:]):
            if node2 == self.sink:
                yield 0
            elif node2.alt > node1.alt:
                yield 1
            elif node2.alt < node1.alt:
                yield -1
            else:
                yield 0

    def bruteforce(self, start_node, start_time, stop_time):
        """Returns a path of (stop_time - start_time + 2) nodes, including the
        starting node"""
        def aux(node, time):
            if time == stop_time:
                best = [0, []]
            else:
                best = max((aux(neigh, time + 1) for neigh in self.g[node]),
                           key=lambda x: x[0])
            # First node doesn't contribute to the score
            if time >= start_time:
                best[0] += self.score(node, time)
            best[1].append(node)
            return best
        return aux(start_node, start_time - 1)

    def test_bruteforce(self):
        score, path = self.bruteforce(self.source, 0, 2)
        path.reverse()
        score2, path2 = self.bruteforce(path[-1], 3, 6)
        path2.reverse()
        print(score, path)
        print(score2, path2)
        print(list(self.path_to_movements(path + path2[1:])))

    def bfs_edges(self, start_node, limit):
        """Produce edges in a breadth-first-search starting at source.
        Modified from networkx to limit to a given distance from the source"""
        def add_mark(node, mark):
            self.g.node[node]["mark"] = mark

        add_mark(start_node, Mark(0, 0, None))
        stack = [(start_node, 0, iter(self.g[start_node]))]
        while stack:
            parent, dist, children = stack[0]
            try:
                child = next(children)
                child_score = self.g.node[parent]["mark"].total_score + self.g.node[child]["nb_targets"]
                # Either we haven't visited the child yet, or we found a better path
                if ("mark" not in self.g.node[child]) or (child_score > self.g.node[child]["mark"].total_score):
                    add_mark(child, Mark(self.g.node[parent]["mark"].last_time + 1, child_score, parent))
                    yield parent, child
                    if dist + 1 < limit:
                        stack.append((child, dist + 1, iter(self.g[child])))
            except StopIteration:
                stack.pop(0)

    def build_path(self, end_node):
        """Build a path, starting from an end node and using the ancestor
        information to go back to the source node."""
        def iterator():
            yield end_node
            parent = self.g.node[end_node]["mark"].ancestor
            while parent != None:
                yield parent
                parent = self.g.node[parent]["mark"].ancestor
        result = list(iterator())
        result.reverse()
        return result

    def test(self, node, limit=10):
        best_node = node
        for e in self.bfs_edges(node, limit):
            mark = self.g.node[e[1]]["mark"]
            #print("{}\n{}\n{}\n".format(e[0], e[1], mark))
            if mark.last_time == limit:
                best_node = max(best_node, e[1], key=lambda n: self.g.node[n]["mark"].total_score)
        print("Best: {} with score {}".format(best_node, self.g.node[best_node]["mark"].total_score))
        path = self.build_path(best_node)
        print(path)
        print(list(self.path_to_movements(path)))
