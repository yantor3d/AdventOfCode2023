"""Advent of Code 2023, Day 09."""

import collections
import itertools

from typing import List


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    sequences = parse(puzzle_input)

    results = map(extrapolate, sequences)

    return sum(results)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    sequences = parse(puzzle_input)
    sequences = [seq[::-1] for seq in sequences]

    results = map(extrapolate, sequences)

    return sum(results)


def parse(puzzle_input: List[str]) -> List[List[int]]:
    """Parse the puzzle input."""

    return [list(map(int, line.strip().split())) for line in puzzle_input]


def extrapolate(values: List[int]) -> int:
    """Extrapolate the next value in the list."""

    rows = collections.deque([values])

    while True:
        row = diff(rows[-1])
        rows.append(row)

        if not any(row):
            break

    new = rows.pop()
    new.append(0)

    while rows:
        old = rows.pop()
        new = undiff(old, new)

    return new[-1]


def diff(values: List[int]) -> List[int]:
    """Return the diffs between each pair of values in the given input.

    Note: The output will have one fewer value than the input.
    """

    lhs = list(itertools.islice(values, 0, None))
    rhs = list(itertools.islice(values, 1, None))

    return [r - l for l, r in zip(lhs, rhs)]


def undiff(old: List[int], new: List[int]) -> List[int]:
    """Return the undiff between trios of values in the given inputs."""

    out = old[:]
    out.append(old[-1] + new[-1])

    return out
