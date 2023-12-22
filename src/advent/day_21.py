"""Advent of Code 2023, Day 21."""

import collections
import functools
import string
import time

from frozendict import frozendict
from typing import Dict, List, Iterator, Set, Tuple

from advent.datatypes import Point

N = Point(+0, -1)
E = Point(+1, +0)
S = Point(+0, +1)
W = Point(-1, +0)

DIRS = frozenset({N, E, W, S})


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    return solve(puzzle_input, 64, inf=False)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    return solve(puzzle_input, 64, inf=True)


def solve(puzzle_input: List[str], num: int) -> int:
    print()

    s, puzzle = parse(puzzle_input)

    return Puzzle(puzzle).count_steps(num, s) + (num % 2 == 0)


def parse(puzzle_input: List[str]) -> Tuple[Point, Dict[Point, str]]:
    result = {}

    s = None

    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            p = Point(x, y)

            if char == "S":
                s = p
                char = "."

            result[p] = char

    return s, frozendict(result)


class Puzzle(object):
    def __init__(self, puzzle: Dict[Point, str]):
        self.puzzle = puzzle
        self.rocks = {p for p, x in puzzle.items() if x == "#"}
        self.mx = max(puzzle)

    def __hash__(self):
        return id(self)

    def count_steps(self, num: int, start: Point) -> int:
        curr = {start: DIRS}

        n = 0

        for i in range(num):
            curr = self.expand(curr)

            if i % 2:
                n += len(curr)

        # pprint(self.puzzle, curr, start)
        # print(num, x)

        return n

    def expand(self, curr: Dict[Point, Set[Point]]) -> Set[Point]:
        result = collections.defaultdict(set)

        for p, dirs in curr.items():
            for d in dirs:
                q = p + d

                if self.is_empty(q):
                    result[q].add(Point(-d.x, -d.y))

        result = {p: DIRS - dirs for p, dirs in result.items()}

        return result

    def is_empty(self, p: Point) -> bool:
        q = self.wrap(p)

        return q not in self.rocks

    def wrap(self, p: Point) -> Point:
        return Point(p.x % (self.mx.x + 1), p.y % (self.mx.y + 1))


def pprint(puzzle: Dict[Point, str], points: Set[Point], start: Point):
    mn = min(puzzle)
    mx = max(puzzle)

    lines = []

    numbers = string.digits + string.ascii_lowercase + string.ascii_uppercase

    for y in range(mn.y, mx.y + 1):
        line = []

        for x in range(mn.x, mx.x + 1):
            p = Point(x, y)

            if p in points:
                char = "O"
            elif p == start:
                char = "$"
            else:
                char = puzzle[p]

            line.append(char)

        lines.append("".join(line))

    print()
    print("\n".join(lines))
