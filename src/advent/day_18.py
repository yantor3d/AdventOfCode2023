"""Advent of Code 2023, Day 18."""

import collections
import operator

from typing import List, Set
from advent.datatypes import Point

Step = collections.namedtuple("Step", "d n")

MOVES = {
    "U": Point(+0, -1),
    "R": Point(+1, +0),
    "D": Point(+0, +1),
    "L": Point(-1, +0),
}

HEX_TO_MOVE = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    steps = parse(puzzle_input, parse_line_01)

    return dig(steps)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    steps = parse(puzzle_input, parse_line_02)

    return dig(steps)


def parse_line_01(line: str) -> Step:
    d, n, _ = line.split()

    return Step(d, int(n))


def parse_line_02(line: str) -> Step:
    _, _, c = line.split()

    nh, dh = c[2:-2], c[-2]

    d = HEX_TO_MOVE[dh]
    n = int(nh, 16)

    return Step(d, n)


def parse(puzzle_input: List[str], parser: callable = parse_line_01) -> List[Step]:
    return list(map(parser, puzzle_input))


def dig(steps: List[Step]) -> int:
    s = Point(0, 0)

    holes = [s]

    for step in steps:
        d = step.d
        m = MOVES.get(d, Point(0, 0))
        n = step.n

        p = holes[-1]
        q = Point(p.x + (m.x * n), p.y + (m.y * n))

        if s == q:
            break

        holes.append(q)

    edges = []

    for i, b in enumerate(holes):
        a = holes[i - 1]

        try:
            c = holes[i + 1]
        except IndexError:
            c = holes[0]

        if False:
            pass
        elif a.x < b.x and b.y > c.y:  # R -> U
            e = Point(b.x + 0, b.y + 0)
        elif a.x < b.x and b.y < c.y:  # R -> D
            e = Point(b.x + 1, b.y + 0)
        elif a.y < b.y and c.x < b.x:  # D -> L
            e = Point(b.x + 1, b.y + 1)
        elif a.y < b.y and b.x < c.x:  # D -> R
            e = Point(b.x + 1, b.y + 0)
        elif a.x > b.x and c.y < b.y:  # L -> U
            e = Point(b.x + 0, b.y + 1)
        elif a.x > b.x and b.y < c.y:  # L -> D
            e = Point(b.x + 1, b.y + 1)
        elif a.y > b.y and c.x < b.x:  # U -> L
            e = Point(b.x + 0, b.y + 1)
        elif a.y > b.y and b.x < c.x:  # U -> R
            e = Point(b.x + 0, b.y + 0)
        else:
            raise RuntimeError(a, b, c)

        edges.append(e)

    a = 0
    b = 0

    for i, p in enumerate(edges):
        try:
            q = edges[i + 1]
        except IndexError:
            q = edges[0]

        a += p.x * q.y
        b += p.y * q.x

    return abs(a - b) // 2
