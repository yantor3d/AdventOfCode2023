"""Test suite for Day 18."""

import pytest

import advent.day_18

from advent.day_18 import Step


@pytest.fixture
def puzzle_input():
    return [
        "R 6 (#70c710)",
        "D 5 (#0dc571)",
        "L 2 (#5713f0)",
        "D 2 (#d2c081)",
        "R 2 (#59c680)",
        "D 2 (#411b91)",
        "L 5 (#8ceee2)",
        "U 2 (#caa173)",
        "L 1 (#1b58a2)",
        "U 2 (#caa171)",
        "R 2 (#7807d2)",
        "U 3 (#a77fa3)",
        "L 2 (#015232)",
        "U 2 (#7a21e3)",
    ]


def test_part_01a(puzzle_input):
    puzzle = advent.day_18.parse(puzzle_input)
    edge = advent.day_18.dig(puzzle)

    assert len(edge) == 38


def test_part_01(puzzle_input):
    answer = advent.day_18.part_01(puzzle_input)

    assert answer == 62


@pytest.mark.parametrize(
    "line,expected",
    [
        ("R 6 (#70c710)", Step("R", 461937)),
        ("D 5 (#0dc571)", Step("D", 56407)),
        ("L 2 (#5713f0)", Step("R", 356671)),
        ("D 2 (#d2c081)", Step("D", 863240)),
        ("R 2 (#59c680)", Step("R", 367720)),
        ("D 2 (#411b91)", Step("D", 266681)),
        ("L 5 (#8ceee2)", Step("L", 577262)),
        ("U 2 (#caa173)", Step("U", 829975)),
        ("L 1 (#1b58a2)", Step("L", 112010)),
        ("U 2 (#caa171)", Step("D", 829975)),
        ("R 2 (#7807d2)", Step("L", 491645)),
        ("U 3 (#a77fa3)", Step("U", 686074)),
        ("L 2 (#015232)", Step("L", 5411)),
        ("U 2 (#7a21e3)", Step("U", 500254)),
    ],
)
def test_parser_02(line, expected):
    actual = advent.day_18.parse_line_02(line)

    assert actual == expected


@pytest.mark.skip
def test_part_02(puzzle_input):
    answer = advent.day_18.part_02(puzzle_input)

    assert answer == 952408144115
