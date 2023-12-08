"""Test suite for Day 08."""

import pytest
import pytest_cases

import advent.day_08


@pytest.fixture(scope="function")
def puzzle_input_01a():
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
def puzzle_input_01b():
    return [
        "LLR",
        "",
        "AAA = (BBB, BBB)",
        "BBB = (AAA, ZZZ)",
        "ZZZ = (ZZZ, ZZZ)",
    ]


@pytest.fixture(scope="function")
def puzzle_input_02():
    return [
        "LR",
        "",
        "11A = (11B, XXX)",
        "11B = (XXX, 11Z)",
        "11Z = (11B, XXX)",
        "22A = (22B, XXX)",
        "22B = (22C, 22C)",
        "22C = (22Z, 22Z)",
        "22Z = (22B, 22B)",
        "XXX = (XXX, XXX)",
    ]


def test_parse_01a(puzzle_input_01a):
    turns, tree = advent.day_08.parse(puzzle_input_01a)

    assert turns == "RL"
    assert set(tree.keys()) == {"AAA", "BBB", "CCC", "DDD", "EEE", "GGG", "ZZZ"}

    assert tree["AAA"] == {"L": "BBB", "R": "CCC"}
    assert tree["BBB"] == {"L": "DDD", "R": "EEE"}
    assert tree["CCC"] == {"L": "ZZZ", "R": "GGG"}
    assert tree["DDD"] == {"L": "DDD", "R": "DDD"}
    assert tree["EEE"] == {"L": "EEE", "R": "EEE"}
    assert tree["GGG"] == {"L": "GGG", "R": "GGG"}
    assert tree["ZZZ"] == {"L": "ZZZ", "R": "ZZZ"}


def test_parse_01b(puzzle_input_01b):
    turns, tree = advent.day_08.parse(puzzle_input_01b)

    assert turns == "LLR"
    assert set(tree.keys()) == {"AAA", "BBB", "ZZZ"}

    assert tree["AAA"] == {"L": "BBB", "R": "BBB"}
    assert tree["BBB"] == {"L": "AAA", "R": "ZZZ"}
    assert tree["ZZZ"] == {"L": "ZZZ", "R": "ZZZ"}


@pytest_cases.pytest_parametrize_plus(
    "puzzle_input,expected",
    [
        [pytest_cases.fixture_ref(puzzle_input_01a), 2],
        [pytest_cases.fixture_ref(puzzle_input_01b), 6],
    ],
    ids=[
        "RL",
        "LLR",
    ],
)
def test_part_01(puzzle_input, expected):
    actual = advent.day_08.part_01(puzzle_input)

    assert actual == expected


def test_parse_02(puzzle_input_02):
    turns, tree = advent.day_08.parse(puzzle_input_02)

    assert turns == "LR"
    assert set(tree.keys()) == {"11A", "11B", "11Z", "22A", "22B", "22C", "22Z", "XXX"}

    assert tree["11A"] == {"L": "11B", "R": "XXX"}
    assert tree["11B"] == {"L": "XXX", "R": "11Z"}
    assert tree["11Z"] == {"L": "11B", "R": "XXX"}
    assert tree["22A"] == {"L": "22B", "R": "XXX"}
    assert tree["22B"] == {"L": "22C", "R": "22C"}
    assert tree["22C"] == {"L": "22Z", "R": "22Z"}
    assert tree["22Z"] == {"L": "22B", "R": "22B"}
    assert tree["XXX"] == {"L": "XXX", "R": "XXX"}


def test_part_02_steps(puzzle_input_02):
    __, tree = advent.day_08.parse(puzzle_input_02)

    ends = ["11Z", "22Z"]

    old_nodes = [None, None]
    new_nodes = ["11A", "22A"]

    old_nodes, new_nodes = advent.day_08.next_02(tree, "L", old_nodes, new_nodes)
    assert new_nodes == ["11B", "22B"]

    old_nodes, new_nodes = advent.day_08.next_02(tree, "R", old_nodes, new_nodes)
    assert new_nodes == ["11Z", "22C"]

    old_nodes, new_nodes = advent.day_08.next_02(tree, "L", old_nodes, new_nodes)
    assert new_nodes == ["11B", "22Z"]

    old_nodes, new_nodes = advent.day_08.next_02(tree, "R", old_nodes, new_nodes)
    assert new_nodes == ["11Z", "22B"]

    old_nodes, new_nodes = advent.day_08.next_02(tree, "L", old_nodes, new_nodes)
    assert new_nodes == ["11B", "22C"]

    old_nodes, new_nodes = advent.day_08.next_02(tree, "R", old_nodes, new_nodes)
    assert new_nodes == ["11Z", "22Z"]


def test_part_02(puzzle_input_02):
    answer = advent.day_08.part_02(puzzle_input_02)

    assert answer == 6
