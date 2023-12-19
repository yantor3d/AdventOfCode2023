"""Test suite for Day 19."""

import pytest

import advent.day_19


@pytest.fixture
def puzzle_input():
    return [
        "px{a<2006:qkq,m>2090:A,rfg}",
        "pv{a>1716:R,A}",
        "lnx{m>1548:A,A}",
        "rfg{s<537:gd,x>2440:R,A}",
        "qs{s>3448:A,lnx}",
        "qkq{x<1416:A,crn}",
        "crn{x>2662:A,R}",
        "in{s<1351:px,qqz}",
        "qqz{s>2770:qs,m<1801:hdj,R}",
        "gd{a>3333:R,R}",
        "hdj{m>838:A,pv}",
        "",
        "{x=787,m=2655,a=1222,s=2876}",
        "{x=1679,m=44,a=2067,s=496}",
        "{x=2036,m=264,a=79,s=2244}",
        "{x=2461,m=1339,a=466,s=291}",
        "{x=2127,m=1623,a=2188,s=1013}",
    ]


@pytest.mark.parametrize(
    "i,out",
    [
        (0, "A"),
        (1, "R"),
        (2, "A"),
        (3, "R"),
        (4, "A"),
    ],
)
def test_part_01_accepted(i, out, puzzle_input):
    workflows, parts = advent.day_19.parse(puzzle_input)

    expected = out == "A"
    actual = advent.day_19.accepted(workflows, parts[i])

    assert actual == expected, parts[i]


@pytest.mark.parametrize(
    "i,expected",
    [
        (0, 7540),
        (2, 4623),
        (4, 6951),
    ],
)
def test_part_01_scores(i, expected, puzzle_input):
    __, parts = advent.day_19.parse(puzzle_input)

    actual = advent.day_19.score(parts[i : i + 1])

    assert actual == expected, parts[i]


def test_part_01(puzzle_input):
    answer = advent.day_19.part_01(puzzle_input)

    assert answer == 19114
