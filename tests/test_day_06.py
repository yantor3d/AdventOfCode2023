"""Test suite for Day 06."""

import pytest

import advent.day_06

PUZZLE_INPUT = [
    "Time:      7  15   30",
    "Distance:  9  40  200",
]


@pytest.fixture(scope="function")
def puzzle_input():
    return PUZZLE_INPUT


def test_parse_01(puzzle_input):
    data = advent.day_06.parse_01(puzzle_input)

    assert data == {
        7: 9,
        15: 40,
        30: 200,
    }


def test_parse_02(puzzle_input):
    data = advent.day_06.parse_02(puzzle_input)

    assert data == {
        71530: 940200,
    }


@pytest.mark.parametrize(
    "hold,expected",
    [
        (0, 0),
        (1, 6),
        (2, 10),
        (3, 12),
        (4, 12),
        (5, 10),
        (6, 6),
        (7, 0),
    ],
    ids=[
        "Hold for 0s",
        "Hold for 1s",
        "Hold for 2s",
        "Hold for 3s",
        "Hold for 4s",
        "Hold for 5s",
        "Hold for 6s",
        "Hold for ys",
    ],
)
def test_run(hold, expected):
    actual = advent.day_06.run(7, hold)

    assert expected == actual


@pytest.mark.parametrize(
    "duration,record,expected",
    [
        (7, 9, (2, 5)),
        (15, 40, (4, 11)),
        (30, 200, (11, 19)),
    ],
    ids=[
        "Win 7s race",
        "Win 15s race",
        "Win 30s race",
    ],
)
def test_win_01(duration, record, expected):
    actual = advent.day_06.win(duration, record)

    assert expected == actual


@pytest.mark.parametrize(
    "duration,record,expected",
    [
        (7, 9, 4),
        (15, 40, 8),
        (30, 200, 9),
    ],
    ids=[
        "Win 7s race 4 ways",
        "Win 15s race 8 ways",
        "Win 30s race 9 ways",
    ],
)
def test_num_wins_01(duration, record, expected):
    mn, mx = advent.day_06.win(duration, record)
    actual = advent.day_06.num_wins(mn, mx)
    assert expected == actual


def test_part_01(puzzle_input):
    answer = advent.day_06.part_01(puzzle_input)

    assert answer == 288


def test_win_02():
    actual = advent.day_06.win(71530, 940200)

    assert actual == (14, 71516)


def test_part_02(puzzle_input):
    answer = advent.day_06.part_02(puzzle_input)

    assert answer == 71503
