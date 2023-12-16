"""Tests for the main functions."""

import advent


def test_get_puzzle_input(get_example_input):
    data = get_example_input(0)

    assert data == ["hello", "world"]


def test_solve(test_source):
    answer_01, answer_02 = advent.solve(0, len, bool, test_source)

    assert answer_01.value == 2
    assert answer_02.value is True
