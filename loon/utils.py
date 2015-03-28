import math
import sys
from collections import namedtuple


Point = namedtuple("Point", ("row", "col"))
Vector = namedtuple("Vector", ("drow", "dcol"))


def bfs_edges_limit(G, source, limit):
        """Produce edges in a breadth-first-search starting at source.
        Modifier from networkx to limit to a given distance from the source"""
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
                

def print_wind(r, c):


    s1 = "/>"
    s2 = "->"
    s3 = "\>"
    s4 = "|,"
    s5 = "|'"
    s6 = "</"
    s7 = "<-"
    s8 = "<\\"

    if (c > 0):
        if (r < 0):
            print(s1, end=' ')
            return
        if (r == 0):
            print(s2, end=' ')
            return
        if (r > 0):
            print(s3, end=' ')
            return
    if (c == 0):
        if (r < 0):
            print(s5, end=' ')
            return
        if (r > 0):
            print(s4, end=' ')
            return
    if (c < 0):
        if (r < 0):
            print(s8, end=' ')
            return
        if (r == 0):
            print(s7, end=' ')
            return
        if (r > 0):
            print(s6, end=' ')
            return
    return
