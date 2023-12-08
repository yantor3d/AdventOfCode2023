"""Test suite for Day 08."""

import pytest
import pytest_cases

import advent.day_08


@pytest.fixture(scope="function")
def puzzle_input():
    return [
        "RL",
        "",
        "AAA = (BBB, CCC)",
        "BBB = (DDD, EEE)",
        "CCC = (ZZZ, GGG)",
        "DDD = (DDD, DDD)",
        "EEE = (EEE, EEE)",
        "GGG = (GGG, GGG)",
        "ZZZ = (ZZZ, ZZZ)",
    ]


@pytest.fixture(scope="function")
def puzzle_input_alt():
    return [
        "LLR",
        "",
        "AAA = (BBB, BBB)",
        "BBB = (AAA, ZZZ)",
        "ZZZ = (ZZZ, ZZZ)",
    ]


def test_parse(puzzle_input):
    turns, tree = advent.day_08.parse(puzzle_input)

    assert turns == "RL"
    assert set(tree.keys()) == {"AAA", "BBB", "CCC", "DDD", "EEE", "GGG", "ZZZ"}

    assert tree["AAA"] == {"L": "BBB", "R": "CCC"}
    assert tree["BBB"] == {"L": "DDD", "R": "EEE"}
    assert tree["CCC"] == {"L": "ZZZ", "R": "GGG"}
    assert tree["DDD"] == {"L": "DDD", "R": "DDD"}
    assert tree["EEE"] == {"L": "EEE", "R": "EEE"}
    assert tree["GGG"] == {"L": "GGG", "R": "GGG"}
    assert tree["ZZZ"] == {"L": "ZZZ", "R": "ZZZ"}


@pytest_cases.pytest_parametrize_plus(
    "lines,expected",
    [
        [pytest_cases.fixture_ref(puzzle_input), 2],
        [pytest_cases.fixture_ref(puzzle_input_alt), 6],
    ],
    ids=[
        "RL",
        "LLR",
    ],
)
def test_part_01(lines, expected):
    actual = advent.day_08.part_01(lines)

    assert actual == expected
