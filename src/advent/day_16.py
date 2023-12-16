"""Advent of Code 2023, Day 16."""

import collections

from typing import Dict, ForwardRef, List, Set, Tuple

Point = ForwardRef("Point")


class Point(collections.namedtuple("Point", "x y")):
    def __lt__(self, other: Point) -> bool:
        return (self.x < other.x) or (self.y < other.y)

    def __gt__(self, other: Point) -> bool:
        return (self.x > other.x) or (self.y > other.y)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


RULES = {
    ".": {"N": "N", "S": "S", "E": "E", "W": "W"},
    "/": {"N": "E", "S": "W", "E": "N", "W": "S"},
    "\\": {"N": "W", "S": "E", "E": "S", "W": "N"},
    "|": {"N": "N", "S": "S", "E": "NS", "W": "NS"},
    "-": {"N": "EW", "S": "EW", "E": "E", "W": "W"},
}

MOVES = {
    "N": Point(0, -1),
    "S": Point(0, 1),
    "E": Point(1, 0),
    "W": Point(-1, 0),
}


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    start = Point(0, 0)

    puzzle = parse(puzzle_input)
    x = run(start, "E", puzzle)

    return x


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    puzzle = parse(puzzle_input)

    n = 0

    for p, d in edges(puzzle):
        x = run(p, d, puzzle)
        n = max(n, x)

    return n


def edges(puzzle):
    mx = max(puzzle)

    # Top left
    yield Point(0, 0), "S"
    yield Point(0, 0), "E"

    # Top row
    for x in range(1, mx.x):
        yield Point(x, 0), "S"

    # Top right
    yield Point(mx.x, 0), "S"
    yield Point(mx.x, 0), "W"

    # Right edge
    for y in range(1, mx.y):
        yield Point(mx.x, y), "W"

    # Bottom left
    yield Point(0, mx.y), "N"
    yield Point(0, mx.y), "E"

    # Bottom row
    for x in range(mx.x, 1, -1):
        yield Point(x, mx.y), "N"

    # Bottom right
    yield Point(mx.x, mx.y), "N"
    yield Point(mx.x, mx.y), "W"

    # Left edge
    for y in range(1, mx.y):
        yield Point(0, y), "E"


def parse(puzzle_input: List[str]) -> Dict[Point, str]:
    result = {}

    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            p = Point(x, y)

            result[p] = char

    return result


def run(start: Point, heading: str, puzzle: Dict[Point, str]) -> int:
    routes = collections.deque([(start, heading)])

    seen = set()

    visited = set()

    while routes:
        p, d = routes.popleft()

        if (p, d) in seen:
            continue

        seen.add((p, d))
        visited.add(p)

        x = puzzle[p]

        rules = RULES[x][d]

        for r in rules:
            m = MOVES[r]
            n = p + m

            try:
                puzzle[n]
            except KeyError:
                continue
            else:
                routes.append((n, r))

    return len(visited)


def dump_route(route):
    print(" > ".join([f"{p.x},{p.y} {d}" for p, d in route]))


def dump_puzzle(puzzle, visited, fp=None):
    mx = max(puzzle)

    lines = []

    for y in range(mx.y + 1):
        line = []
        for x in range(mx.x + 1):
            line.append(".")
        lines.append(line)

    for p in visited:
        lines[p.y][p.x] = "#"

    lines = ["".join(line) for line in lines]

    for line in lines:
        print(line, file=fp)
