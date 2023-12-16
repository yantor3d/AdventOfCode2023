"""Advent of Code 2023, Day 16."""

from __future__ import annotations

import collections
import functools

from typing import Iterator, List, Set, Tuple


class Point(collections.namedtuple("Point", "x y")):
    def __lt__(self, other: Point) -> bool:
        return (self.x < other.x) or (self.y < other.y)

    def __gt__(self, other: Point) -> bool:
        return (self.x > other.x) or (self.y > other.y)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


Move = Tuple[Point, str]


class Puzzle(dict):
    """A grid of tiles with symbols."""

    def __hash__(self) -> int:
        return id(self)

    def run(self, s: Point, d: str) -> int:
        routes = collections.deque([(s, d)])

        seen = set()
        visited = set()

        while routes:
            p, d = routes.popleft()

            if (p, d) in seen:
                continue

            seen.add((p, d))

            n, v = self.go(p, d)

            routes.extend(n)
            visited.update(v)

        return len(visited)

    @functools.cache
    def go(self, s: Point, d: str) -> Tuple[List[Move], Set[Move]]:
        result = []
        visited = set()
        p = s

        while True:
            try:
                x = self[p]
            except KeyError:
                break
            else:
                visited.add(p)

            rules = RULES[x][d]

            if rules == d:
                m = MOVES[rules]
                p = p + m
            else:
                for r in rules:
                    m = MOVES[r]
                    n = p + m

                    if n in self:
                        result.append((n, r))
                break

        return result, visited

    def edges(self) -> Iterator[Move]:
        mx = max(self)

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
    x = puzzle.run(start, "E")

    return x


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    puzzle = parse(puzzle_input)

    n = 0

    for p, d in list(puzzle.edges()):
        x = puzzle.run(p, d)
        n = max(n, x)

    return n


def parse(puzzle_input: List[str]) -> Puzzle:
    result = {}

    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            p = Point(x, y)

            result[p] = char

    return Puzzle(result)
