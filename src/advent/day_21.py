"""Advent of Code 2023, Day 21."""

import collections
import string

from typing import Dict, List, Iterator, Set, Tuple

from advent.datatypes import Point


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    s, puzzle = parse(puzzle_input)

    return get_steps(64, s, puzzle)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


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


def get_steps(
    num: int,
    start: Point,
    puzzle: Dict[Point, str],
    adjacent_fn: callable = None,
) -> int:
    adjacent_fn = adjacent_fn or adjacent_fin

    mx = max(puzzle)

    old = collections.Counter()
    old[start, 0] = 0

    for i in range(num):
        new = collections.Counter(old)
        for (p, s) in list(old):
            for q, loop in adjacent_fn(p, mx):
                if puzzle.get(q) == ".":
                    new[(q, i + 1)] += 1

        old = {(p, s): n for (p, s), n in new.items() if s == i + 1}

    return len(old)


def adjacent_fin(p: Point, mx: Point) -> Iterator[Tuple[Point, bool]]:
    for q in p.adjacent():
        yield q, False


def adjacent_inf(p: Point, mx: Point) -> Iterator[Tuple[Point, bool]]:
    for q in p.adjacent():
        n = True

        if q.x < 0:
            q = Point(mx.x, q.y)
        elif q.y < 0:
            q = Point(q.x, mx.y)
        elif q.x > mx.x:
            q = Point(0, q.y)
        elif q.y > mx.y:
            q = Point(q.x, 0)
        else:
            q = q
            n = False

        yield q, n


def pprint(puzzle: Dict[Point, str], points: Dict[Tuple[Point, int], int], start: Point):
    mn = min(puzzle)
    mx = max(puzzle)

    lines = []

    points = {p: s for (p, s), n in points.items()}

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
