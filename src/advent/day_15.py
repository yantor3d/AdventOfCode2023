"""Advent of Code 2023, Day 15."""

from typing import List


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    steps = []

    for line in puzzle_input:
        steps.extend(line.split(","))

    hashes = map(hash_of, steps)

    return sum(hashes)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def hash_of(chars: str):
    result = 0

    for char in chars:
        result += ord(char)
        result *= 17
        result %= 256

    return result
