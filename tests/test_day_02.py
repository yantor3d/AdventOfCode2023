"""Test suite for Day 02."""

import pytest

import advent.day_02

from advent.day_02 import Cubes, CUBES


@pytest.fixture(scope="function")
def puzzle_input():
    return [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]


@pytest.mark.parametrize(
    "expected,line",
    [
        (True, "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"),
        (True, "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"),
        (False, "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"),
        (False, "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red"),
        (True, "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"),
    ],
    ids=[
        "Game 1",
        "Game 2",
        "Game 3",
        "Game 4",
        "Game 5",
    ],
)
def test_part_01_lines(line, expected):
    game = advent.day_02.get_results(line)
    actual = advent.day_02.is_game_possible(game, CUBES)

    assert actual == expected


def test_part_01(puzzle_input):
    actual = advent.day_02.part_01(puzzle_input)

    assert actual == 8
