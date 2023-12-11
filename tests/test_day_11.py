"""Test suite for Day 11."""

import pytest

import advent.day_11

from advent.day_11 import Point


@pytest.fixture(scope="function")
def puzzle_input():
    return [
        "...#......",
        ".......#..",
        "#.........",
        "..........",
        "......#...",
        ".#........",
        ".........#",
        "..........",
        ".......#..",
        "#...#.....",
    ]


def test_iter_items():
    items = "abcd"

    items = list(advent.day_11.iter_items(items, [1, 3]))

    assert items == [(0, "a"), (1, "b"), (2, "b"), (3, "c"), (4, "d"), (5, "d")]


def test_parse_as_is(puzzle_input):
    result, mn, mx = advent.day_11.parse(puzzle_input, expand=False)

    output = advent.day_11.dump(result, mn, mx)

    assert output == [
        "...1......",
        ".......2..",
        "3.........",
        "..........",
        "......4...",
        ".5........",
        ".........6",
        "..........",
        ".......7..",
        "8...9.....",
    ]


def test_parse_expand(puzzle_input):
    result, mn, mx = advent.day_11.parse(puzzle_input, expand=True)

    output = advent.day_11.dump(result, mn, mx)

    assert output == [
        "....1........",
        ".........2...",
        "3............",
        ".............",
        ".............",
        "........4....",
        ".5...........",
        "............6",
        ".............",
        ".............",
        ".........7...",
        "8....9.......",
    ]


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (Point(1, 6), Point(5, 11), 9),
        (Point(4, 0), Point(9, 10), 15),
        (Point(0, 2), Point(12, 7), 17),
        (Point(0, 11), Point(5, 11), 5),
    ],
    ids=[
        "Galaxy 5 -> 9 in 9 steps",
        "Galaxy 1 -> 7 in 15 steps",
        "Galaxy 3 -> 6 in 17 steps",
        "Galaxy 8 -> 9 in 5 steps",
    ],
)
def test_shortest_path(a, b, expected):
    mn = Point(0, 0)
    mx = Point(15, 15)

    path = advent.day_11.shortest_path(a, b, mn, mx)

    assert (len(path) - 1) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (Point(1, 6), Point(5, 11), 9),
        (Point(4, 0), Point(9, 10), 15),
        (Point(0, 2), Point(12, 7), 17),
        (Point(0, 11), Point(5, 11), 5),
    ],
    ids=[
        "Galaxy 5 -> 9 in 9 steps",
        "Galaxy 1 -> 7 in 15 steps",
        "Galaxy 3 -> 6 in 17 steps",
        "Galaxy 8 -> 9 in 5 steps",
    ],
)
def test_shortcut(a, b, expected):
    actual = advent.day_11.shortcut(a, b)

    assert actual == expected


def test_part_01(puzzle_input):
    answer = advent.day_11.part_01(puzzle_input)

    assert answer == 374
