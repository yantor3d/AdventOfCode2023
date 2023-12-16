"""Test suite for Day 16."""

import pytest

import advent.day_16


@pytest.fixture()
def puzzle_input(get_example_input):
    return get_example_input(16)


def test_part_01(puzzle_input):
    answer = advent.day_16.part_01(puzzle_input)

    assert answer == 46


def test_part_02(puzzle_input):
    answer = advent.day_16.part_02(puzzle_input)

    assert answer == 51
