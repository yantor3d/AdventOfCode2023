"""Advent of Code 2023, Day 17."""

from __future__ import annotations

import functools
import heapq
import sys

from typing import Dict, List, Set
from advent.datatypes import Point

Maze = Dict[Point, int]

MOVES = {
    "N": Point(0, -1),
    "S": Point(0, +1),
    "E": Point(+1, 0),
    "W": Point(-1, 0),
}


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    maze = parse(puzzle_input)

    return run(maze, 1, 3)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    maze = parse(puzzle_input)

    return run(maze, 4, 10)


def parse(puzzle_input: List[str]) -> Maze:
    return {
        Point(x, y): int(col) for y, row in enumerate(puzzle_input) for x, col in enumerate(row)
    }


def run(maze: Maze, mn: int, mx: int) -> int:
    s = min(maze)
    e = max(maze)

    result = sys.maxsize
    seen = set()

    pq = [
        (0, s, MOVES["S"]),
        (0, s, MOVES["E"]),
    ]

    while pq:
        h, p, d = heapq.heappop(pq)

        if p == e:
            result = h
            break

        if (p, d) in seen:
            continue

        seen.add((p, d))

        for m in moves(d):
            q, y = p, h

            for i in range(1, mx + 1):
                q = ptoq(q, m)

                if q not in maze:
                    continue

                y += maze[q]

                if i >= mn and (q, m) not in seen:
                    heapq.heappush(pq, (y, q, m))

    return result


@functools.cache
def moves(d: Point) -> Set[Point]:
    b = Point(-d.x, -d.y)
    return set(MOVES.values()) - {d, b}


@functools.cache
def ptoq(p: Point, m: Point) -> Point:
    return Point(p.x + m.x, p.y + m.y)
