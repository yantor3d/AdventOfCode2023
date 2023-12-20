"""Test suite for Day 20."""

import pytest

import advent.day_20


@pytest.fixture()
def puzzle_input_a():
    return [
        "broadcaster -> a, b, c",
        "%a -> b",
        "%b -> c",
        "%c -> inv",
        "&inv -> a",
    ]


@pytest.fixture()
def puzzle_input_b():
    return [
        "broadcaster -> a",
        "%a -> inv, con",
        "&inv -> b",
        "%b -> con",
        "&con -> output",
    ]


def test_parse(puzzle_input_a):
    modules = advent.day_20.parse(puzzle_input_a)

    assert set(modules) == {"broadcaster", "a", "b", "c", "inv"}
    assert modules["broadcaster"].outputs == ["a", "b", "c"]
    assert modules["inv"].outputs == ["a"]
    assert modules["a"].outputs == ["b"]
    assert modules["b"].outputs == ["c"]
    assert modules["c"].outputs == ["inv"]


def test_example_a(puzzle_input_a):
    modules = advent.day_20.parse(puzzle_input_a)

    lo, hi = advent.day_20.run(modules, verbose=False)

    assert (lo * hi) == 32
    assert modules["a"].state is False
    assert modules["b"].state is False
    assert modules["c"].state is False


def test_example_b(puzzle_input_b):
    modules = advent.day_20.parse(puzzle_input_b)

    verbose = False

    advent.day_20.run(modules, verbose)

    assert modules["a"].state is True
    assert modules["b"].state is True
    assert modules["con"].state == {"a": "high", "b": "high"}

    advent.day_20.run(modules, verbose)

    assert modules["a"].state is False
    assert modules["b"].state is True
    assert modules["con"].state == {"a": "low", "b": "high"}

    advent.day_20.run(modules, verbose)

    assert modules["a"].state is True
    assert modules["b"].state is False
    assert modules["con"].state == {"a": "high", "b": "low"}

    advent.day_20.run(modules, verbose)

    assert modules["a"].state is False
    assert modules["b"].state is False
    assert modules["con"].state == {"a": "low", "b": "low"}


def test_part_01a(puzzle_input_a):
    answer = advent.day_20.part_01(puzzle_input_a)

    assert answer == 32000000


def test_part_01b(puzzle_input_b):
    answer = advent.day_20.part_01(puzzle_input_b)

    assert answer == 11687500
