"""Advent of Code 2023, Day 08."""

import itertools
import re

from typing import Dict, List, Tuple


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    result = 0

    turns, tree = parse(puzzle_input)
    old = "AAA"
    new = None

    for i, turn in enumerate(itertools.cycle(turns), 1):
        if i > 100000:
            raise RuntimeError(i)

        new = tree[old][turn]

        result = i

        if new == "ZZZ":
            break
        else:
            old = new

    return result


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def parse(puzzle_input: List[str]) -> Tuple[List[str], Dict]:
    turns = []
    tree = {}

    lines = iter(puzzle_input)

    turns = next(lines).strip()
    next(lines)

    for line in lines:
        tree.update(parse_line(line))

    return turns, tree


def parse_line(line: str) -> Dict:
    name, lf, rt = re.findall(r"\w{3}", line)

    return {name: {"L": lf, "R": rt}}
