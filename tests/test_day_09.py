"""Test suite for Day 0."""

import pytest

import advent.day_09


@pytest.fixture(scope="function")
def puzzle_input():
    return [
        "0 3 6 9 12 15",
        "1 3 6 10 15 21",
        "10 13 16 21 30 45",
    ]


@pytest.mark.parametrize(
    "values,expected",
    [
        ([0, 3, 6, 9, 12, 15], [3, 3, 3, 3, 3]),
        ([3, 3, 3, 3, 3], [0, 0, 0, 0]),
    ],
    ids=[
        "first diff",
        "second diff",
    ],
)
def test_diff_01(values, expected):
    actual = advent.day_09.diff(values)

    assert expected == actual


@pytest.mark.parametrize(
    "old,new,expected",
    [
        ([0, 3, 6, 9, 12, 15], [3, 3, 3, 3, 3, 3], 18),
        ([2, 3, 4, 5, 6], [1, 1, 1, 1, 1], 7),
    ],
)
def test_undiff_01(old, new, expected):
    actual = advent.day_09.undiff(old, new)

    assert actual[-1] == expected


@pytest.mark.parametrize(
    "values,expected",
    [
        ([0, 3, 6, 9, 12, 15], 18),
        ([1, 3, 6, 10, 15, 21], 28),
        ([10, 13, 16, 21, 30, 45], 68),
    ],
    ids=[
        "first",
        "second",
        "third",
    ],
)
def test_extrapolate_01(values, expected):
    actual = advent.day_09.extrapolate(values)

    assert actual == expected


def test_part_01(puzzle_input):
    answer = advent.day_09.part_01(puzzle_input)

    assert answer == 114


@pytest.mark.parametrize(
    "values,expected",
    [
        ([0, 3, 6, 9, 12, 15], -3),
        ([1, 3, 6, 10, 15, 21], 0),
        ([10, 13, 16, 21, 30, 45], 5),
    ],
    ids=[
        "first",
        "second",
        "third",
    ],
)
def test_extrapolate_02(values, expected):
    actual = advent.day_09.extrapolate(values[::-1])

    assert actual == expected


def test_part_02(puzzle_input):
    answer = advent.day_09.part_02(puzzle_input)

    assert answer == 2
