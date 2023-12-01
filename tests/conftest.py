"""Advent of Code 2023 test suite config."""

from typing import List

import pytest

import advent


@pytest.fixture(scope="function")
def test_source():
    return r"tests\_data"


@pytest.fixture(scope="function")
def get_example_input(test_source) -> callable:
    def fn(day: int) -> List[str]:
        return advent.get_puzzle_input(day, test_source)

    return fn
