"""Advent of Code 2023, Day 01."""


def part_01(puzzle_input):
    values = map(get_value, puzzle_input)

    return sum(values)


def part_02(puzzle_input):
    return


def get_value(line: str) -> int:
    """Return the calibration value from the given line."""

    numbers = [x for x in line if str.isdigit(x)]

    first = numbers[0]
    last = numbers[-1]

    return int(f"{first}{last}")
