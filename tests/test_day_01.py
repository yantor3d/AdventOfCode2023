"""Test suite for Day 01."""

import advent.day_01


def test_part_01():
    puzzle_input = [
        "1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet",
    ]

    answer = advent.day_01.part_01(puzzle_input)

    assert answer == 142
