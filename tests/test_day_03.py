"""Test suite for Day 03."""

import pytest

import advent.day_03


@pytest.fixture(scope="function")
def puzzle_input():
    return [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]


def test_parse_part_01(puzzle_input):
    numbers = advent.day_03.parse_01(puzzle_input)

    assert numbers == [467, 35, 633, 617, 592, 755, 664, 598]


def test_part_01(puzzle_input):
    answer = advent.day_03.part_01(puzzle_input)

    assert answer == 4361


def test_parse_part_02(puzzle_input):
    gears = advent.day_03.parse_02(puzzle_input)

    assert gears == [(467, 35), (755, 598)]


def test_part_02(puzzle_input):
    answer = advent.day_03.part_02(puzzle_input)

    assert answer == 467835
