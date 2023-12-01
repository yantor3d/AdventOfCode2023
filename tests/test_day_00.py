"""Tests for the main functions."""

import advent


def test_get_puzzle_input():
    data = advent.get_puzzle_input(0, 'tests/data')

    assert data == ['hello', 'world']


def test_solve():
    answer_01, answer_02 = advent.solve(0, len, bool, 'tests/data')

    assert answer_01 == 2
    assert answer_02 is True
