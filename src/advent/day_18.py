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
    edge = dig(steps)
    hole = cut(edge)

    return len(hole)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    steps = parse(puzzle_input, parse_line_02)
    edge = dig(steps)
    hole = cut(edge)

    return len(hole)


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
