"""Advent of Code 2023, Day 21."""

import collections

from typing import Dict, List, Set, Tuple

from advent.datatypes import Point


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    s, puzzle = parse(puzzle_input)

    result = get_steps(64, s, puzzle)

    return len(result)


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


def get_steps(num: int, start: Point, puzzle: Dict[Point, str]) -> Set[Point]:
    old = {start}

    for _ in range(num):
        new = set()
        for p in old:
            for q in p.adjacent():
                if puzzle.get(q) == ".":
                    new.add(q)
        old = new

    return old


def pprint(puzzle: Dict[Point, str], points: List[Point], start: Point):
    mn = min(puzzle)
    mx = max(puzzle)

    lines = []

    for y in range(mn.y, mx.y + 1):
        line = []

        for x in range(mn.x, mx.x + 1):
            p = Point(x, y)

            if p in points:
                char = "O"
            elif p == start:
                char = "S"
            else:
                char = puzzle[p]

            line.append(char)

        lines.append("".join(line))

    print()
    print("\n".join(lines))
