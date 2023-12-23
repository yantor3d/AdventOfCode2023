"""Advent of Code 2023, Day 21."""

import collections
import functools
import string
import time

from typing import Dict, List, Iterator, Set, Tuple

from advent.datatypes import Point

N = Point(+0, -1)
E = Point(+1, +0)
S = Point(+0, +1)
W = Point(-1, +0)

DIRS = frozenset({N, E, W, S})


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    return solve(puzzle_input, 64)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    s, puzzle = parse(puzzle_input)

    puzzle = Puzzle(puzzle)

    side = len(puzzle_input)
    half = s.x

    x0 = half
    x1 = half + side
    x2 = half + (2 * side)

    f0, f1, f2 = puzzle.walk((x0, x1, x2), s)

    # System of equations:
    # f(0) = a*0^2 + b*0 + c = f0, so  c     = f0
    # f(1) = a*1^2 + b*1 + c = f1,
    #      = a     + b   + c = f1, so  a + b = f1 - f0
    # f(2) = a*2^2 + b*2 + c = f2
    #      = 4a    + 2b  + c = f2, so 4a + 2b = f2 - f0
    # Gauss elimination gives:        2a      = f2 - f0 - 2*(f1 - f0) = f2 - 2f1 + f0
    # This gives:                           b = f1 - f0 - a

    c = f0
    a = (f2 - 2 * f1 + f0) // 2
    b = f1 - f0 - a

    f = lambda n: a * n**2 + b * n + c
    x = (26501365 - half) // side

    return f(x)


def solve(puzzle_input: List[str], num: int) -> int:
    s, puzzle = parse(puzzle_input)

    return Puzzle(puzzle).walk([num], s)[0]


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

    return s, result


class Puzzle(object):
    def __init__(self, puzzle: Dict[Point, str]):
        self.puzzle = puzzle
        self.rocks = {p for p, x in puzzle.items() if x == "#"}
        self.mx = max(puzzle)

    def __hash__(self):
        return id(self)

    def walk(self, steps: List[int], start: Point) -> List[int]:
        result = []

        x, y = start
        visited = {start: 0}
        d = 0

        queue = collections.deque()
        queue.append(start)

        for d in range(1, max(steps) + 1):
            tmp = collections.deque()

            while queue:
                p = queue.popleft()

                for m in (N, S, E, W):
                    q = p + m

                    if q in visited:
                        continue

                    if self.is_empty(q):
                        visited[q] = d
                        tmp.append(q)

            queue = tmp

            if d in steps:
                result.append(sum((x % 2 == d % 2 for x in visited.values())))

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
