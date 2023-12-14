"""Test suite for Day 14."""

import pytest

import advent.day_14


@pytest.fixture()
def puzzle_input():
    return [
        "O....#....",
        "O.OO#....#",
        ".....##...",
        "OO.#O....O",
        ".O.....O#.",
        "O.#..O.#.#",
        "..O..#O..O",
        ".......O..",
        "#....###..",
        "#OO..#....",
    ]


def test_tilt_north(puzzle_input):
    old = puzzle_input
    new = advent.day_14.tilt(old)

    assert new == [
        "OOOO.#.O..",
        "OO..#....#",
        "OO..O##..O",
        "O..#.OO...",
        "........#.",
        "..#....#.#",
        "..O..#.O.O",
        "..O.......",
        "#....###..",
        "#....#....",
    ]


def test_part_01(puzzle_input):
    answer = advent.day_14.part_01(puzzle_input)

    assert answer == 136
