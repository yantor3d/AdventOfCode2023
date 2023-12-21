"""Test suite for Day 21."""

import pytest
import time

import advent.day_21
from advent.day_21 import Point


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
    answer = advent.day_21.solve(puzzle_input, 6, inf=False)

    assert answer == 16


@pytest.mark.parametrize(
    "p,expected",
    (
        #              -1,-0        +1,+0        +0,+1        +0,-1
        (Point(0, 0), {Point(2, 0), Point(1, 0), Point(0, 1), Point(0, 2)}),
        (Point(1, 0), {Point(0, 0), Point(2, 0), Point(1, 1), Point(1, 2)}),
        (Point(2, 0), {Point(1, 0), Point(0, 0), Point(2, 1), Point(2, 2)}),
        (Point(0, 1), {Point(2, 1), Point(1, 1), Point(0, 2), Point(0, 0)}),
        (Point(1, 1), {Point(0, 1), Point(2, 1), Point(1, 2), Point(1, 0)}),
        (Point(2, 1), {Point(1, 1), Point(0, 1), Point(2, 2), Point(2, 0)}),
        (Point(0, 2), {Point(2, 2), Point(1, 2), Point(0, 0), Point(0, 1)}),
        (Point(1, 2), {Point(0, 2), Point(2, 2), Point(1, 0), Point(1, 1)}),
        (Point(2, 2), {Point(1, 2), Point(0, 2), Point(2, 0), Point(2, 1)}),
    ),
    ids=[
        "Top Left",
        "Top",
        "Top Right",
        "Left",
        "Center",
        "Right",
        "Bottom Left",
        "Bottom",
        "Bottom Right",
    ],
)
def xest_adjacent_inf(p, expected):
    actual = advent.day_21.adjacent_inf(p, Point(2, 2))
    actual = [p for (p, n) in actual]

    assert set(actual) == set(expected)


@pytest.mark.parametrize(
    "n,expected",
    (
        (6, 16),
        (10, 50),
        (50, 1594),
        # (100, 6536),
        # (1000, 668697),
        # (5000, 16733044),
    ),
)
def test_part_02(puzzle_input, n, expected):
    st = time.time()
    actual = advent.day_21.solve(puzzle_input, n, inf=True)
    et = time.time()

    print(f"Solved {n} steps in {et - st:.2f} seconds.")

    assert actual == expected
