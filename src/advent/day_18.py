"""Advent of Code 2023, Day 18."""

import collections
import operator

from typing import List, Set
from advent.datatypes import Point

Step = collections.namedtuple("Step", "d n color")

MOVES = {
    "U": Point(+0, -1),
    "R": Point(+1, +0),
    "D": Point(+0, +1),
    "L": Point(-1, +0),
}


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    steps = parse(puzzle_input)
    edge = dig(steps)
    hole = cut(edge)

    return len(hole)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def parse(puzzle_input: List[str]) -> List[Step]:
    return list(map(parse_line, puzzle_input))


def parse_line(line: str) -> Step:
    d, n, c = line.split()

    return Step(d, int(n), c[1:-1])


def dig(steps: List[Step]) -> List[Point]:
    p = Point(0, 0)

    result = {p}

    for step in steps:
        m = MOVES[step.d]

        for _ in range(step.n):
            p = p + m
            result.add(p)

    return result


def cut(perimeter: List[Point]) -> List[Point]:
    result = set(perimeter)

    x = min(perimeter)

    queue = collections.deque()
    queue.append(x + Point(1, 1))
    seen = set()

    while queue:
        p = queue.popleft()

        if p in seen:
            continue

        seen.add(p)
        result.add(p)

        for a in p.adjacent():
            if p not in perimeter:
                queue.append(a)

    return result


def pprint(holes: List[Point]) -> None:
    xs = [p.x for p in holes]
    ys = [p.y for p in holes]

    mn = Point(min(xs), min(ys))
    mx = Point(max(xs), max(ys))

    lines = [
        ["#" if Point(x, y) in holes else "." for x in range(mn.x, mx.x + 1)]
        for y in range(mn.y, mx.y + 1)
    ]

    lines = ["".join(line) for line in lines]
    lines = "\n".join(lines)

    print(lines)
