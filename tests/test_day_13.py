"""Test suite for Day 13."""

import pytest

import advent.day_13


@pytest.fixture()
def puzzle_input():
    return [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
        "",
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ]


def test_parse(puzzle_input):
    patterns = advent.day_13.parse(puzzle_input)

    assert len(patterns) == 2
    assert patterns[0] == [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ]

    assert patterns[1] == [
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ]


@pytest.mark.parametrize(
    "lines,expected",
    [
        (
            [
                "#####.##.",
                "#####.##.",
            ],
            True,
        ),
        (
            [
                "..##..###",
                "#####.##.",
                "#####.##.",
                "..##..###",
            ],
            True,
        ),
        (
            [
                "#....#..#",
                "..##..###",
                "#####.##.",
                "#####.##.",
                "..##..###",
                "#....#..#",
            ],
            True,
        ),
        (
            [
                "#...##..#",
                "#....#..#",
                "..##..###",
                "#####.##.",
                "#####.##.",
                "..##..###",
            ],
            False,
        ),
    ],
    ids=[
        "Pattern 1, Rows 4:5 True",
        "Pattern 1, Rows 3:6 True",
        "Pattern 1, Rows 2:7 True",
        "Pattern 1, Rows 1:6 False",
    ],
)
def test_is_mirror_image(lines, expected):
    actual = advent.day_13.is_mirror_image(lines)

    assert actual == expected


@pytest.mark.parametrize(
    "n,expected",
    [(0, ("v", (5, 6))), (1, ("h", (4, 5)))],
    ids=[
        "Pattern 1, Vertical between Columns 5/6",
        "Pattern 2, Horizontal between Rows 4/5",
    ],
)
def test_reflections(puzzle_input, n, expected):
    patterns = advent.day_13.parse(puzzle_input)
    pattern = patterns[n]
    actual = advent.day_13.find_reflection(pattern)

    assert actual == expected


@pytest.mark.parametrize(
    "reflection,expected",
    [(("v", (5, 6)), 5), (("h", (4, 5)), 400)],
    ids=[
        "Vertical",
        "Horizontal",
    ],
)
def test_score(reflection, expected):
    actual = advent.day_13.score(reflection)

    assert actual == expected


def test_part_01(puzzle_input):
    answer = advent.day_13.part_01(puzzle_input)

    assert answer == 405
