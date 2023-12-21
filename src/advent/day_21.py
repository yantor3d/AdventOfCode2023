"""Advent of Code 2023, Day 21."""

import collections
import functools
import string
import time

from typing import Dict, List, Iterator, Set, Tuple

from advent.datatypes import Point


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    return solve(puzzle_input, 64, inf=False)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    return solve(puzzle_input, 64, inf=True)


def solve(puzzle_input: List[str], num: int, inf: bool = False) -> int:
    adjacent_fn = adjacent_inf if inf else adjacent_fin

    s, puzzle = parse(puzzle_input)
    puzzle = Puzzle(puzzle, num, adjacent_fn)
    result = puzzle.get_steps(num, s)

    return score(result)


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


def edges(mx: Point) -> Iterator[Point]:
    for x in range(mx.x):
        yield Point(x, 0)

    for y in range(1, mx.y):
        yield Point(0, y)
        yield Point(mx.x, y)

    for x in range(mx.x):
        yield Point(x, mx.y)


class Puzzle(object):
    def __init__(self, puzzle: Dict[Point, str], num: int, adjacent_fn: callable = None):
        self.puzzle = puzzle
        self.mx = max(puzzle)
        self.num = num
        self.adjacent_fn = adjacent_fn or adjacent_fin

    @functools.cache
    def get_steps(
        self, num: int, start: Point, tile: Point = Point(0, 0)
    ) -> Dict[Point, Set[Point]]:
        result = collections.defaultdict(set)

        if num == 0:
            result[tile].add(start)
            return result

        old = set()
        old.add(start)

        for i in range(num):
            new = set()

            for p in list(old):
                for q, t in self.adjacent_fn(p, self.mx, tile):
                    if self.puzzle.get(q) != ".":
                        continue

                    if t == tile:
                        new.add(q)
                    else:
                        recurse = self.get_steps(num - i - 1, q)
                        recurse = {k + t: v for k, v in recurse.items()}

                        result = merge(result, recurse)

            old = new
            result[tile] = new

        return result


def merge(lhs: Dict[Point, Set[Point]], rhs: Dict[Point, Set[Point]]):
    result = collections.defaultdict(set)

    for k, v in lhs.items():
        result[k].update(v)

    for k, v in rhs.items():
        result[k].update(v)

    return result


def score(result: Dict[Point, Set[Point]]):
    return sum(map(len, result.values()))


def adjacent_fin(p: Point, mx: Point, t: Point = Point(0, 0)) -> Iterator[Tuple[Point, Point]]:
    for q in p.adjacent():
        yield q, t


@functools.cache
def adjacent_inf(p: Point, mx: Point, t: Point = Point(0, 0)) -> List[Tuple[Point, Point]]:
    result = []

    for q in p.adjacent():
        if q.x < 0:
            q = Point(mx.x, q.y)
            u = Point(t.x - 1, t.y)
        elif q.y < 0:
            q = Point(q.x, mx.y)
            u = Point(t.x, t.y - 1)
        elif q.x > mx.x:
            q = Point(0, q.y)
            u = Point(t.x + 1, t.y)
        elif q.y > mx.y:
            q = Point(q.x, 0)
            u = Point(t.x, t.y + 1)
        else:
            q = q
            u = t

        result.append((q, u))

    return result


def pprint(puzzle: Dict[Point, str], points: Dict[Tuple[Point, int], int], start: Point):
    mn = min(puzzle)
    mx = max(puzzle)

    lines = []

    points = {p: n for (p, s), n in points.items()}

    numbers = string.digits + string.ascii_lowercase + string.ascii_uppercase

    for y in range(mn.y, mx.y + 1):
        line = []

        for x in range(mn.x, mx.x + 1):
            p = Point(x, y)

            if p in points:
                char = numbers[points[p]]
            elif p == start:
                char = "$"
            else:
                char = puzzle[p]

            line.append(char)

        lines.append("".join(line))

    print()
    print(points.values())
    print("\n".join(lines))
