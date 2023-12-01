"""Test suite for Day 01."""

import pytest

import advent.day_01


@pytest.mark.parametrize(
    "line,expected",
    [
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77),
    ],
)
def test_part_01_lines(line, expected):
    actual = advent.day_01.get_value(advent.day_01.find_digits, line)

    assert actual == expected


def test_part_01():
    puzzle_input = [
        "1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet",
    ]

    answer = advent.day_01.part_01(puzzle_input)

    assert answer == 142


@pytest.mark.parametrize(
    "line,expected",
    [
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76),
    ],
)
def test_part_02_lines(line, expected):
    actual = advent.day_01.get_value(advent.day_01.find_numbers, line)

    assert actual == expected


def test_part_02():
    puzzle_input = [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ]

    answer = advent.day_01.part_02(puzzle_input)

    assert answer == 281
