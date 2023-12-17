"""Advent of Code 2023, Day 17."""

from __future__ import annotations

import collections
import operator
import heapq
import sys

from frozendict import frozendict
from queue import PriorityQueue
from typing import Dict, List, Set, Tuple

from advent.datatypes import Point

Maze = Dict[Point, int]
Graph = Dict[Tuple[Point, str, int], Set[Tuple[Point, str, int]]]

Vertex = collections.namedtuple("Vertex", "p d n")

MOVES = {
    "N": Point(0, -1),
    "S": Point(0, +1),
    "E": Point(+1, 0),
    "W": Point(-1, 0),
}

RULES = {
    "N": "NEW",
    "S": "SEW",
    "E": "ENS",
    "W": "WNS",
}


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    maze = parse(puzzle_input)

    return run(maze)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def parse(puzzle_input: List[str]) -> Maze:
    return {
        Point(x, y): int(col) for y, row in enumerate(puzzle_input) for x, col in enumerate(row)
    }


def run(maze: Maze) -> Graph:
    s = min(maze)
    e = max(maze)

    distances = get_distances(maze, s, e)

    return min(distances)


def get_distances(maze: Maze, s: Point, e: Point) -> Dict[Vertex, int]:
    distances = collections.defaultdict(lambda: sys.maxsize)

    pq = [
        (0, Vertex(s, "S", 0)),
        (0, Vertex(s, "E", 0)),
    ]

    while pq:
        old_dist, old_vert = heapq.heappop(pq)

        if old_dist > distances[old_vert]:
            continue

        p, d, n = old_vert

        for r in RULES[old_vert.d]:
            if d == r:
                u = n + 1
            else:
                u = 1

            if u > 3:
                continue

            m = MOVES[r]
            q = Point(p.x + m.x, p.y + m.y)

            if q not in maze:
                continue

            new_vert = Vertex(q, r, u)
            new_dist = old_dist + maze[q]

            if new_dist < distances[new_vert]:
                distances[new_vert] = new_dist
                heapq.heappush(pq, (new_dist, new_vert))

    result = []

    for vert, dist in distances.items():
        if vert.p == e:
            result.append(dist)

    return result
