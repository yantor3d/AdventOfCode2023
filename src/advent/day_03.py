"""Advent of Code 2023, Day 03."""

import uuid

from typing import Dict, Set


class PartNumber(object):
    """Engine schematic part number."""

    def __init__(self, value=0, indexes=None):
        """Initialize."""

        self.indexes = indexes or []
        self.value = value
        self._id = uuid.uuid4().hex

    def __repr__(self):
        """Return a repr of this number."""

        return f"{self.__class__.__name__}(value={self.value}, indexes={self.indexes})"


def part_01(puzzle_input):
    """Solve part one."""

    part_numbers = parse_01(puzzle_input)

    return sum(part_numbers)


def part_02(puzzle_input):
    """Solve part two."""


def parse_01(lines):
    """Find the numbers adjacent to a symbol in the given lines."""

    numbers = {}
    symbols = {}

    for y, line in enumerate(lines):
        numbers.update(find_numbers(line, y))

        for x, char in enumerate(line):
            if char == ".":
                continue
            elif str.isdigit(char):
                continue
            else:
                symbols[(y, x)] = char

    return find_part_numbers(numbers, symbols)


def find_numbers(line: str, y: int) -> Dict:
    """Return the part numbers in the given line."""

    parts = [PartNumber()]

    for i, char in enumerate(line):
        if str.isdigit(char):
            parts[-1].indexes.append(i)
            parts[-1].value = (parts[-1].value * 10) + int(char)
        else:
            parts.append(PartNumber())

    result = {}

    for part in parts:
        for x in part.indexes:
            result[(y, x)] = part

    return result


def find_part_numbers(numbers: Dict, symbols: Dict) -> Set[int]:
    """Return the part numbers (numbers adjacent to a symbol)."""

    results = []
    seen = set()

    for (y, x), number in sorted(numbers.items()):
        for key in adjacent(y, x):
            try:
                symbols[key]
            except KeyError:
                continue
            else:
                if number._id not in seen:
                    seen.add(number._id)
                    results.append(number.value)
                    break

    return results


def adjacent(y: int, x: int):
    """Yield the cells adjacent to the given coordinates."""

    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if (dy, dx) == (0, 0):
                continue

            ay, ax = y + dy, x + dx

            yield ay, ax
