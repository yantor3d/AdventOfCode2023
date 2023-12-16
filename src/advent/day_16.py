"""Advent of Code 2023, Day 16."""

import collections

from typing import Dict, ForwardRef, List, Tuple

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
    visited = run(start, puzzle)

    return len(visited)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def parse(puzzle_input: List[str]) -> Dict[Point, str]:
    result = {}

    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            p = Point(x, y)

            result[p] = char

    return result


def run(start: Point, puzzle: Dict[Point, str]) -> int:
    routes = collections.deque([[(start, "E")]])

    visited = collections.defaultdict(list)

    seen = set()

    nv = []

    while routes:
        route = routes.popleft()

        p, d = route[-1]

        if (p, d) in seen:
            continue

        seen.add((p, d))

        visited[p].append(d)

        x = puzzle[p]

        rules = RULES[x][d]

        for r in rules:
            m = MOVES[r]
            n = p + m

            new_route = [i for i in route]
            new_route.append((n, r))

            try:
                puzzle[n]
                routes.append(new_route)
            except KeyError:
                continue

        nv.append(len(visited))

    return visited


def dump_route(route):
    print(" > ".join([f"{p.x},{p.y} {d}" for p, d in route]))


def dump_puzzle(puzzle, visited, fp):
    mx = max(puzzle)

    lines = []

    for y in range(mx.y + 1):
        line = []
        for x in range(mx.x + 1):
            line.append(".")
        line.append("\n")
        lines.append(line)

    arrows = {
        "N": "^",
        "S": "v",
        "E": ">",
        "W": "<",
    }

    for p, moves in visited.items():
        lines[p.y][p.x] = "#"

    lines = ["".join(line) for line in lines]

    fp.writelines(lines)
