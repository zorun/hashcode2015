import math
import sys
from collections import namedtuple


Point = namedtuple("Point", ("row", "col"))
Vector = namedtuple("Vector", ("drow", "dcol"))


def bfs_edges_limit(G, source, limit):
    """Produce edges in a breadth-first-search starting at source.
    Modified from networkx to limit to a given distance from the source"""
    visited = set([source])
    stack = [(source, 0, iter(G[source]))]
    while stack:
        parent, dist, children = stack[0]
        if dist > limit:
            stack.pop(0)
        else:
            try:
                child = next(children)
                if child not in visited:
                    yield parent,child
                    visited.add(child)
                    stack.append((child, dist + 1, iter(G[child])))
            except StopIteration:
                stack.pop(0)

def sign(x):
    if x == 0:
        return 0
    else:
        return 1 if x > 0 else -1

def get_wind(vec):
    """Returns an arrow representing the wind direction given by a vector"""
    directions = {
        (0,   0) : "·",
        (1,   0) : "̉↑",
        (1,   1) : "↗",
        (0,   1) : "→",
        (-1,  1) : "↘",
        (-1,  0) : "↓",
        (-1, -1) : "↙",
        (0,  -1) : "←",
        (1,  -1) : "↖"
    }
    return directions[(sign(vec.drow), sign(vec.dcol))]
