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

    points, mn, mx = parse(puzzle_input, expand=True)

    n = 0

    for a, b in itertools.combinations(points, 2):
        n += shortcut(a, b)

    return n


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


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


def parse(puzzle_input: List[str], expand=True) -> List[Point]:
    result = []

    if expand:
        num_rows = len(puzzle_input)
        num_cols = len(puzzle_input[0])

        empty_rows = [row for row in range(num_rows) if is_row_empty(puzzle_input, row)]
        empty_cols = [col for col in range(num_cols) if is_col_empty(puzzle_input, col)]
    else:
        empty_rows = []
        empty_cols = []

    for y, line in iter_items(puzzle_input, empty_rows):
        for x, char in iter_items(line, empty_cols):
            if char == "#":
                p = Point(int(x), int(y))

                result.append(p)

    return result, Point(0, 0), Point(x, y)


def is_row_empty(puzzle_input: List[str], row: int) -> bool:
    """Return True if the given row is empty."""

    return set(puzzle_input[row]) == {"."}


def is_col_empty(puzzle_input: List[str], col: int) -> bool:
    """Return True if the given column is empty."""

    return {line[col] for line in puzzle_input} == {"."}


def iter_items(items: List, double_indexes: List[int]):
    """Yield the given items, once normally, twice at the given indexes."""

    index = itertools.count()

    for i, item in enumerate(items):
        if i in double_indexes:
            yield next(index), item
            yield next(index), item
        else:
            yield next(index), item


def shortcut(a: Point, b: Point) -> int:
    return abs(b.x - a.x) + abs(b.y - a.y)


def shortest_path(a: Point, b: Point, mn: Point, mx: Point):
    queue = collections.deque()

    visited = set()
    dist = {a: 0}
    prev = {}

    queue.append(a)
    visited.add(a)

    while queue:
        p = queue.popleft()

        for n in neighbors(p):
            if n < mn:
                continue

            if n > mx:
                continue

            if n not in visited:
                visited.add(n)
                dist[n] = dist[p] + 1
                prev[n] = p

                queue.append(n)

        if b in visited:
            break

    path = []
    n = b

    while n != a:
        path.append(n)
        n = prev[n]

    path.append(a)
    path.reverse()

    return path


def neighbors(p: Point) -> Iterator[Point]:
    yield Point(p.x + 1, p.y + 0)
    yield Point(p.x + 0, p.y + 1)
    yield Point(p.x - 1, p.y + 0)
    yield Point(p.x + 0, p.y - 1)
