"""Test suite for Day 12."""

import pytest

import advent.day_12


@pytest.fixture(scope="function")
def puzzle_input():
    return [
        "???.### 1,1,3",
        ".??..??...?##. 1,1,3",
        "?#?#?#?#?#?#?#? 1,3,1,6",
        "????.#...#... 4,1,1",
        "????.######..#####. 1,6,5",
        "?###???????? 3,2,1",
    ]


@pytest.mark.parametrize(
    "line,blocks,expected",
    [
        ("???.###", (1, 1, 3), 1),
        (".??..??...?##.", (1, 1, 3), 4),
        ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), 1),
        ("????.#...#...", (4, 1, 1), 1),
        ("????.######..#####.", (1, 6, 5), 4),
        ("?###????????", (3, 2, 1), 10),
    ],
)
def test_num_solutions_01(line, blocks, expected):
    actual = advent.day_12.num_solutions(line + ".", blocks)

    assert actual == expected


def test_part_01(puzzle_input):
    answer = advent.day_12.part_01(puzzle_input)

    assert answer == 21


@pytest.mark.parametrize(
    "line,blocks,expected",
    [
        ("???.###", (1, 1, 3), 1),
        (".??..??...?##.", (1, 1, 3), 16384),
        ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), 1),
        ("????.#...#...", (4, 1, 1), 16),
        ("????.######..#####.", (1, 6, 5), 2500),
        ("?###????????", (3, 2, 1), 506250),
    ],
)
def test_num_solutions_02(line, blocks, expected):
    line, blocks = advent.day_12.unfold(line, blocks)
    actual = advent.day_12.num_solutions(line + ".", blocks)

    assert actual == expected


def test_part_02(puzzle_input):
    answer = advent.day_12.part_02(puzzle_input)

    assert answer == 525152
