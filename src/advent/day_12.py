"""Advent of Code 2023, Day 12."""

import collections
import itertools

from typing import Iterator, List, Set, Tuple


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    values = parse(puzzle_input)

    n = 0

    for line, checksum in values:
        result = get_arrangements(line, checksum)

        n += len(result)

    return n


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def parse(puzzle_input: List[str]) -> List:
    result = []

    for line in puzzle_input:
        line, numbers = line.split()

        checksum = tuple(map(int, numbers.split(",")))

        result.append((line, checksum))

    return result


def get_arrangements(line: str, checksum: Tuple[int]) -> Set[str]:
    """Return the possible arrangements for the line."""

    result = set()

    queue = collections.deque([line])

    while queue:
        line = queue.popleft()

        if is_repaired(line):
            if get_checksum(line) == checksum:
                result.add(line)
        else:
            queue.extend(get_repairs(line))

    return result


def get_checksum(line: str) -> Tuple[int]:
    """Return the condition record checksum."""

    groups = []
    group = []

    for char in line:
        if char == ".":
            if group:
                groups.append(group)
                group = []
        elif char == "#":
            group.append(char)
    else:
        if group:
            groups.append(group)

    return tuple([len(grp) for grp in groups])


def get_repairs(line: str) -> Iterator[str]:
    """Yield the ways in which the given line could be repaired."""

    if "?" in line:
        yield line.replace("?", ".", 1)
        yield line.replace("?", "#", 1)


def is_repaired(line: str) -> bool:
    """Return True if the line has been repaired."""

    return "?" not in line
