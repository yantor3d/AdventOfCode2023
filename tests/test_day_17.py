"""Test suite for Day 18."""

import pytest

import advent.day_17


@pytest.fixture
def puzzle_input():
    return [
        "2413432311323",
        "3215453535623",
        "3255245654254",
        "3446585845452",
        "4546657867536",
        "1438598798454",
        "4457876987766",
        "3637877979653",
        "4654967986887",
        "4564679986453",
        "1224686865563",
        "2546548887735",
        "4322674655533",
    ]


def test_part_01(puzzle_input):
    answer = advent.day_17.part_01(puzzle_input)

    assert answer == 102


def test_part_02a(puzzle_input):
    answer = advent.day_17.part_02(puzzle_input)

    assert answer == 94


def test_part_02b():
    example = [
        "111111111111",
        "999999999991",
        "999999999991",
        "999999999991",
        "999999999991",
    ]
    answer = advent.day_17.part_02(example)

    assert answer == 71
