"""Test suite for Day 15."""

import pytest

import advent.day_15


@pytest.fixture
def puzzle_input():
    return ["rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"]


def test_hash():
    result = advent.day_15.hash_of("HASH")

    assert result == 52


@pytest.mark.parametrize(
    "chars,expected",
    (
        ("rn=1", 30),
        ("cm-", 253),
        ("qp=3", 97),
        ("cm=2", 47),
        ("qp-", 14),
        ("pc=4", 180),
        ("ot=9", 9),
        ("ab=5", 197),
        ("pc-", 48),
        ("pc=6", 214),
        ("ot=7", 231),
    ),
)
def test_hashes_01(chars, expected):
    actual = advent.day_15.hash_of(chars)

    assert expected == actual


def test_part_01(puzzle_input):
    answer = advent.day_15.part_01(puzzle_input)

    assert answer == 1320


@pytest.mark.parametrize(
    "box_number,lenses,expected",
    (
        [0, {"rn": 1, "cm": 2}, 5],
        [3, {"ot": 7, "ab": 5, "pc": 6}, 140],
    ),
)
def test_focusing_power(box_number, lenses, expected):
    actual = advent.day_15.focusing_power(box_number, lenses)

    assert expected == actual


def test_part_02(puzzle_input):
    answer = advent.day_15.part_02(puzzle_input)

    assert answer == 145
