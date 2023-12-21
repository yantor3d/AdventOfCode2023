"""Test suite for Day 21."""

import pytest

import advent.day_21


@pytest.fixture
def puzzle_input():
    return [
        "...........",
        ".....###.#.",
        ".###.##..#.",
        "..#.#...#..",
        "....#.#....",
        ".##..S####.",
        ".##..#...#.",
        ".......##..",
        ".##.#.####.",
        ".##..##.##.",
        "...........",
    ]


def test_part_01(puzzle_input):
    s, puzzle = advent.day_21.parse(puzzle_input)

    result = advent.day_21.get_steps(6, s, puzzle)

    assert len(result) == 16
