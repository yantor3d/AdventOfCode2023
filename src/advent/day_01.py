"""Advent of Code 2023, Day 01."""

from typing import List

import functools
import re

NUMBERS = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}


def part_01(puzzle_input):
    """Return the sum of the calibration values

    The calibration values are the first and last digit in each line.
    """

    fn = functools.partial(get_value, find_digits)

    return sum(map(fn, puzzle_input))


def part_02(puzzle_input):
    """Return the sum of the calibration values

    The calibration values are the first and last number or digit in each line.
    """

    fn = functools.partial(get_value, find_numbers)

    return sum(map(fn, puzzle_input))


def find_digits(line: str) -> List[int]:
    """Return the digits in the given string."""

    return [x for x in line if str.isdigit(x)]


def find_numbers(line: str) -> List[int]:
    """Return the numbers in the given string as digits."""

    numbers = {}

    for digit, number in sorted(NUMBERS.items()):
        for match in re.finditer(number, line):
            numbers[match.start()] = digit

    for idx, char in enumerate(line):
        if str.isdigit(char):
            numbers[idx] = int(char)

    digits = [v for __, v in sorted(numbers.items())]

    return digits


def get_value(fn: callable, line: str) -> int:
    """Return the calibration value from the given line."""

    digits = fn(line)

    first = digits[0]
    last = digits[-1]

    return int(f"{first}{last}")
