"""Test suite for Day 22."""

import pytest

import advent.day_22

from advent.day_22 import Block, Point


@pytest.fixture
def puzzle_input():
    return [
        "1,0,1~1,2,1",
        "0,0,2~2,0,2",
        "0,2,3~2,2,3",
        "0,0,4~0,2,4",
        "2,0,5~2,2,5",
        "0,1,6~2,1,6",
        "1,1,8~1,1,9",
    ]


def test_parse(puzzle_input):
    blocks = advent.day_22.parse(puzzle_input)

    assert len(blocks) == 7


@pytest.mark.skip
def test_view_xz(puzzle_input):
    blocks = advent.day_22.parse(puzzle_input)

    advent.day_22.xz_view(blocks)


@pytest.mark.skip
def test_view_yz(puzzle_input):
    blocks = advent.day_22.parse(puzzle_input)

    advent.day_22.yz_view(blocks)


def test_fall(puzzle_input):
    blocks = advent.day_22.parse(puzzle_input)

    blocks = advent.day_22.fall(blocks)
    blocks = {b.name: b for b in blocks}

    assert blocks["A"] == Block("A", Point(1, 0, 1), Point(1, 2, 1))
    assert blocks["B"] == Block("B", Point(0, 0, 2), Point(2, 0, 2))
    assert blocks["C"] == Block("C", Point(0, 2, 2), Point(2, 2, 2))
    assert blocks["D"] == Block("D", Point(0, 0, 3), Point(0, 2, 3))
    assert blocks["E"] == Block("E", Point(2, 0, 3), Point(2, 2, 3))
    assert blocks["F"] == Block("F", Point(0, 1, 4), Point(2, 1, 4))
    assert blocks["G"] == Block("G", Point(1, 1, 5), Point(1, 1, 6))
    # advent.day_22.xz_view(blocks)
    # advent.day_22.yz_view(blocks)


def test_rest(puzzle_input):
    blocks = advent.day_22.parse(puzzle_input)
    blocks = advent.day_22.fall(blocks)

    above, below = advent.day_22.rest(blocks)

    assert above == {
        "A": set(),
        "B": {"A"},
        "C": {"A"},
        "D": {"B", "C"},
        "E": {"B", "C"},
        "F": {"D", "E"},
        "G": {"F"},
    }

    assert below == {
        "A": {"B", "C"},
        "B": {"D", "E"},
        "C": {"D", "E"},
        "D": {"F"},
        "E": {"F"},
        "F": {"G"},
        "G": set(),
    }


def test_dust(puzzle_input):
    blocks = advent.day_22.parse(puzzle_input)
    blocks = advent.day_22.fall(blocks)

    result = advent.day_22.dust(blocks)

    assert result == {"B", "C", "D", "E", "G"}


def test_part_01(puzzle_input):
    answer = advent.day_22.part_01(puzzle_input)

    assert answer == 5
