"""Advent of Code 2023, Day 11."""

import collections
import itertools
import sys

from typing import Dict, Iterator, List, Tuple


class Point(collections.namedtuple("Point", "x y")):
    def __lt__(self, other):
        return (self.x < other.x) or (self.y < other.y)

    def __gt__(self, other):
        return (self.x > other.x) or (self.y > other.y)


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    return solve(puzzle_input, expand=2)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    return solve(puzzle_input, expand=1000000)


def solve(puzzle_input: List[str], expand=0) -> int:
    points, mn, mx = parse(puzzle_input, expand)

    n = 0

    for a, b in itertools.combinations(points, 2):
        n += shortcut(a, b)

    return n


def dump(points: List[Point], mn: Point, mx: Point, path: List[Point] = None) -> List[str]:
    lines = []

    for _ in range(mn.y, mx.y + 1):
        line = ["." for _ in range(mn.x, mx.x + 1)]
        lines.append(line)

    for p in path or []:
        lines[p.y][p.x] = "#"

    for i, p in enumerate(points, 1):
        lines[p.y][p.x] = str(i)

    return ["".join(line) for line in lines]


def parse(puzzle_input: List[str], expand: int = 0) -> List[Point]:
    points = []

    if expand:
        num_rows = len(puzzle_input)
        num_cols = len(puzzle_input[0])

        empty_rows = [row for row in range(num_rows) if is_row_empty(puzzle_input, row)]
        empty_cols = [col for col in range(num_cols) if is_col_empty(puzzle_input, col)]
    else:
        empty_rows = []
        empty_cols = []

    if expand:
        expand -= 1

    y_offset = 0

    for y, line in enumerate(puzzle_input):
        if y in empty_rows:
            y_offset += expand

        x_offset = 0

        for x, char in enumerate(line):
            if x in empty_cols:
                x_offset += expand

            if char == "#":
                p = Point(int(x) + x_offset, int(y) + y_offset)

                points.append(p)

    mn, mx = Point(0, 0), Point(x + x_offset, y + y_offset)

    return points, mn, mx


def is_row_empty(puzzle_input: List[str], row: int) -> bool:
    """Return True if the given row is empty."""

    return set(puzzle_input[row]) == {"."}


def is_col_empty(puzzle_input: List[str], col: int) -> bool:
    """Return True if the given column is empty."""

    return {line[col] for line in puzzle_input} == {"."}


def iter_items(items: List, double_indexes: List[int], expand=0):
    """Yield the given items, once normally, twice at the given indexes."""

    index = itertools.count()

    for i, item in enumerate(items):
        if i in double_indexes:
            for _ in range(expand):
                yield next(index), item
        else:
            yield next(index), item


def shortcut(a: Point, b: Point) -> int:
    return abs(b.x - a.x) + abs(b.y - a.y)
