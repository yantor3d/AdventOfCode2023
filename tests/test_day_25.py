"""Test suite for Day 25."""

import pytest

import advent.day_25


@pytest.fixture
def puzzle_input():
    return [
        "jqt: rhn xhk nvd",
        "rsh: frs pzl lsr",
        "xhk: hfx",
        "cmg: qnr nvd lhk bvb",
        "rhn: xhk bvb hfx",
        "bvb: xhk hfx",
        "pzl: lsr hfx nvd",
        "qnr: nvd",
        "ntq: jqt hfx bvb xhk",
        "nvd: lhk",
        "lsr: lhk",
        "rzs: qnr cmg lsr rsh",
        "frs: qnr lhk lsr",
    ]


@pytest.fixture
def cuts_01():
    return [
        frozenset({"hfx", "pzl"}),
        frozenset({"bvb", "cmg"}),
        frozenset({"nvd", "jqt"}),
    ]


def test_parse(puzzle_input):
    nodes = advent.day_25.parse(puzzle_input)

    assert len(nodes) == 15


def test_min_cut(puzzle_input):
    nodes = advent.day_25.parse(puzzle_input)

    subnets = advent.day_25.min_cut(nodes)

    assert len(subnets) == 2
    assert subnets[0] == {"bvb", "hfx", "jqt", "ntq", "rhn", "xhk"}
    assert subnets[1] == {"cmg", "frs", "lhk", "lsr", "nvd", "pzl", "qnr", "rsh", "rzs"}


def test_part_01(puzzle_input):
    nodes = advent.day_25.parse(puzzle_input)

    answer = advent.day_25.solve_01(nodes)

    assert answer == 54
