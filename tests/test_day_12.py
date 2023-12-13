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
    "line,expected",
    [
        ("#.#.###", (1, 1, 3)),
        (".#...#....###.", (1, 1, 3)),
        (".#.###.#.######", (1, 3, 1, 6)),
        ("####.#...#...", (4, 1, 1)),
        ("#....######..#####.", (1, 6, 5)),
        (".###.##....#", (3, 2, 1)),
    ],
)
def test_get_checksum(line, expected):
    actual = advent.day_12.get_checksum(line)

    assert expected == actual, line


@pytest.mark.parametrize(
    "line,expected",
    [
        ("???.###", [".??.###", "#??.###"]),
        (".??.###", ["..?.###", ".#?.###"]),
        ("..?.###", ["....###", "..#.###"]),
        ("..#.###", []),
    ],
)
def test_get_repairs(line, expected):
    actual = list(advent.day_12.get_repairs(line))

    assert expected == actual


@pytest.mark.parametrize(
    "line,checksum,expected",
    [
        ("???.###", (1, 1, 3), {"#.#.###"}),
        (
            ".??..??...?##.",
            (1, 1, 3),
            {"..#...#...###.", ".#....#...###.", "..#..#....###.", ".#...#....###."},
        ),
    ],
)
def test_get_arrangements(line, checksum, expected):
    actual = advent.day_12.get_arrangements(line, checksum)

    assert expected == actual


@pytest.mark.parametrize(
    "line,checksum,expected",
    [
        ("???.###", (1, 1, 3), 1),
        (".??..??...?##.", (1, 1, 3), 4),
        ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), 1),
        ("????.#...#...", (4, 1, 1), 1),
        ("????.######..#####.", (1, 6, 5), 4),
        ("?###????????", (3, 2, 1), 10),
    ],
)
def test_num_arrangements(line, checksum, expected):
    actual = advent.day_12.get_arrangements(line, checksum)

    assert expected == len(actual)


def test_part_01(puzzle_input):
    answer = advent.day_12.part_01(puzzle_input)

    assert answer == 21
