"""Advent of Code 2023, Day 03."""

import collections
import uuid

from typing import Dict, Iterator, List, Tuple


class PartNumber(object):
    """Engine schematic part number."""

    def __init__(self, value: int = 0, indexes: List[int] = None):
        """Initialize."""

        self.indexes = indexes or []
        self.value = value
        self._id = uuid.uuid4().hex

    def __repr__(self) -> str:
        """Return a repr of this number."""

        return f"{self.__class__.__name__}(value={self.value}, indexes={self.indexes})"


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    part_numbers = parse_01(puzzle_input)

    return sum(part_numbers)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    part_numbers = parse_02(puzzle_input)
    gear_ratios = [a * b for a, b in part_numbers]

    return sum(gear_ratios)


def parse(lines: List[str]) -> Tuple[Dict, Dict]:
    """Parse the puzzle input."""

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

    return numbers, symbols


def parse_01(lines: List[str]) -> List[int]:
    """Find the numbers adjacent to a symbol in the given lines."""

    numbers, symbols = parse(lines)

    part_numbers = find_part_numbers(numbers, symbols)

    results = collections.ChainMap(*(parts for parts in part_numbers.values()))

    return list(sorted(results.values()))


def parse_02(lines: List[str]) -> List[Tuple[int, int]]:
    """Find pairs of numbers adjcent to a gear (*) symbol."""

    numbers, symbols = parse(lines)

    return find_gears(numbers, symbols)


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


def find_part_numbers(numbers: Dict, symbols: Dict) -> Dict:
    """Return the part numbers adjacent to a symbol."""

    results = collections.defaultdict(dict)

    for (y, x), number in sorted(numbers.items()):
        for key in adjacent(y, x):
            try:
                symbols[key]
            except KeyError:
                continue
            else:
                results[key][number._id] = number.value

    return results


def find_gears(numbers: Dict, symbols: Dict) -> List[Tuple[int, int]]:
    """Return part number pairs adjacent to a gear (*) symbol."""

    results = []
    part_numbers = find_part_numbers(numbers, symbols)

    for key, parts in sorted(part_numbers.items()):
        if symbols[key] == "*" and len(parts) == 2:
            results.append(tuple(parts.values()))

    return results


def adjacent(y: int, x: int) -> Iterator[Tuple[int, int]]:
    """Yield the cells adjacent to the given coordinates."""

    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if (dy, dx) == (0, 0):
                continue

            ay, ax = y + dy, x + dx

            yield ay, ax
